import requests

from urllib.parse import urlparse

from bs4 import BeautifulSoup

from scrapper.models import Job, Skill, JobSkill, ParsedProfile


class Counter(object):
    counter = 0
    limit = 20
    parsed = []


class JobSkillScrapper(object):
    bs = None
    url = None

    def __init__(self, url):
        self.data = {}
        self.next_urls = []

        self.url = self.transform_url(url)
        if Counter.counter >= Counter.limit:
            return None

        Counter.parsed.append(url)
        parsedprofile, created = ParsedProfile.objects.get_or_create(url=self.url)

        # Initializing fake browser to bypass LinkedIn security
        try:
            r = requests.request('GET', self.url, headers=self.headers)
        except Exception:
            pass
        else:
            self.set_html(r.text)
            self.parse(created)

    def set_html(self, text):
        self.bs = BeautifulSoup(text, 'html.parser')

    def transform_url(self, url):
        url = urlparse(url)
        return 'http://' + url.netloc + url.path

    def parse(self, not_parsed):
        """ Parse LinkedIn profile """
        print('Parsing profile : {}'.format(self.url))

        if not_parsed:
            self.parse_jobs()
            self.parse_skills()
            self.persist()
        else:
            print('> Already parsed')
        self.parse_next_profiles()

    def persist(self):
        """ Save jobs and skills into database """

        # Persist profil with at least one job and four skills
        if self.data['jobs'] and len(self.data['skills']) >= 3:
            Counter.counter += 1

            jobs = []
            for job_name in self.data['jobs']:
                job, created = Job.objects.get_or_create(name=job_name)
                jobs.append(job)

            skills = []
            for skill_name in self.data['skills']:
                skill, created = Skill.objects.get_or_create(name=skill_name)
                skills.append(skill)

            msg = '> Persisted - {} job(s) - {} skill(s)'

            jobskills = []
            for job in jobs:
                for skill in skills:
                    jobskills.append(JobSkill(job=job, skill=skill))
            JobSkill.objects.bulk_create(jobskills)
        else:
            msg = '> Not persisted - {} job(s) - {} skill(s)'
        print(msg.format(len(self.data['jobs']), len(self.data['skills'])))


class LinkedInJobSkillScrapper(JobSkillScrapper):
    """ Allow to parse public LinkedIn profile and retrieve data """
    headers = {
        'Host': 'www.linkedin.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.linkedin.com/',
        'X-IsAJAXForm': '1',
        'x-requested-with': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    def parse_jobs(self):
        """ Parse jobs """
        self.data['jobs'] = []

        bs_jobs = self.bs.find(id='experience')
        if bs_jobs:
            for bs_job in bs_jobs.find_all(class_='position'):
                bs_job_title = bs_job.find('h4')
                if bs_job_title:
                    self.data['jobs'].append(bs_job_title.get_text().lower())

    def parse_skills(self):
        """ Parse skills """
        self.data['skills'] = []

        bs_skills = self.bs.find(id='skills')
        if bs_skills:
            for bs_skill in bs_skills.find_all(class_='skill'):
                self.data['skills'].append(bs_skill.get_text().lower())

    def parse_next_profiles(self):
        bs_browse_map = self.bs.find(class_='browse-map')
        if bs_browse_map:
            for bs_profile_card in bs_browse_map.find_all(class_='profile-card'):
                url = self.transform_url(bs_profile_card.find('a').get('href'))
                if url not in Counter.parsed:
                    LinkedInJobSkillScrapper(url)


class ViadeoJobSkillScrapper(JobSkillScrapper):
    """ Allow to parse public Viadeo profile and retrieve data """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-IsAJAXForm': '1',
        'x-requested-with': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    def is_valid_url(self, url):
        return url.startswith('http://fr.viadeo.com/fr/')

    def parse_jobs(self):
        """ Parse jobs """
        self.data['jobs'] = []

        bs_jobs = self.bs.find('ul', id='memberContent')
        if bs_jobs:
            for bs_job in bs_jobs.find_all('li', class_='blockitemEmployment'):
                bs_job_title = bs_job.find('p', class_='titre')
                if bs_job_title:
                    self.data['jobs'].append(bs_job_title.get_text().lower())

    def parse_skills(self):
        """ Parse skills """
        self.data['skills'] = []

        bs_skills = self.bs.find('div', id='sectionPublicSkill')
        if bs_skills:
            for bs_skill in bs_skills.find_all('li', class_='isMemberSkill'):
                self.data['skills'].append(bs_skill.get_text().lower())

    def parse_next_profiles(self):
        bs_browse_map = self.bs.find('ul', id='alsoVisitedTarget')
        if bs_browse_map:
            for bs_profile_card in bs_browse_map.find_all('li', class_='contact'):
                url = self.transform_url(bs_profile_card.find('a').get('href'))
                if self.is_valid_url(url) and url not in Counter.parsed:
                    self.next_urls.append(url)


class ScrapperHandler(object):
    def __init__(self, service, urls):
        scrapper = LinkedInJobSkillScrapper if service == 'linkedin' else ViadeoJobSkillScrapper

        next_urls = []
        for url in urls:
            obj = scrapper(url)
            next_urls += obj.next_urls

        if next_urls:
            ScrapperHandler(service, next_urls)
