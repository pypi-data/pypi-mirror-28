import pyoozie


class OozieClient:
    base_url = 'http://localhost:11000/oozie'

    def __init__(self, base_url):
        self.base_url = base_url

    def run_workflow(self, xml_path, configuration):
        c = pyoozie.OozieClient(self.base_url)
        job_id = c.jobs_submit_workflow(xml_path, configuration=configuration, start=True)
        return job_id


    def run_coordinator(self, xml_path, configuration):
        c = pyoozie.OozieClient(self.base_url)
        job_id = c.jobs_submit_coordinator(xml_path, configuration=configuration)
        return job_id
