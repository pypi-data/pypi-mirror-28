import pyoozie


class OozieClient:
    base_url = 'http://localhost:11000/oozie'
    user = 'hdfs'

    def __init__(self, base_url, user="hdfs"):
        self.base_url = base_url
        self.user = user

    def create_oozie_client(self):
        return pyoozie.OozieClient(url=self.base_url, user=self.user)

    def run_workflow(self, xml_path, configuration):
        c = self.create_oozie_client()
        job_id = c.jobs_submit_workflow(xml_path, configuration=configuration, start=True)
        return job_id

    def run_coordinator(self, xml_path, configuration):
        c = self.create_oozie_client()
        job_id = c.jobs_submit_coordinator(xml_path, configuration=configuration)
        return job_id
