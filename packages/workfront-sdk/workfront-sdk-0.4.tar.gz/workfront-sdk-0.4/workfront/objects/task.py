from workfront.exceptions import WFException
from workfront.objects.codes import WFObjCode
from workfront.objects import user
from workfront.objects.generic_objects import WFParamValuesObject
import workfront.objects.project


class WFTask(WFParamValuesObject):
    '''
    @summary: A Workfront Task helper class
    '''

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param idd: worfront id of the task
        '''
        super(WFTask, self).__init__(wf, WFObjCode.task, idd)

    def set_status(self, status):
        '''
        @summary: Hit WF to set the status of the current task.
        @param status: one of the WFTaskStatus
        '''
        r = self.wf.put_object(WFObjCode.task, self.wf_id, {"status": status})
        if r.status_code != 200:
            err = "When setting status {} to task {}: {}"
            err = err.format(status, self.wf_id, r.json())
            raise WFException(err)

    def get_status(self):
        '''
        @return: the status of the current task ( can be one of the
        WFTaskStatus)
        '''
        r = self.wf.get_object(WFObjCode.task, self.wf_id, ["status"])
        return r.json()["data"]["status"]

    def assign_to_user(self, user):
        '''
        @summary: Assign the current task to the given user.
        @param user: an instance of WFUser
        '''
        params = {
            "objID": user.wf_id,
            "objCode": WFObjCode.user
        }
        r = self.wf.action(WFObjCode.task, self.wf_id, "assign", params)
        if r.status_code != 200:
            err = "When assigning user {} to task {}: {}"
            err = err.format(user.wf_id, self.wf_id, r.json())
            raise WFException(err)

    def get_assigned_user(self):
        '''
        @return: an instance of the user (WFUser object) that is assigned to
        the current task.
        '''
        r = self.wf.get_object(WFObjCode.task, self.wf_id,
                               ["assignments:assignedTo:*"])
        if r.status_code != 200:
            err = "When getting assigned user from task {}: {}"
            err = err.format(self.wf_id, r.json())
            raise WFException(err)
        u = user.WFUser(self.wf, js=r["data"]["assignments"][0]["assignedTo"])
        return u

    def get_project(self):
        r = self.wf.get_object(WFObjCode.task, self.wf_id, ["project:ID"])
        if r.status_code != 200:
            err = "When user from task {}: {}"
            err = err.format(self.wf_id, r.json())
            raise WFException(err)

        proj_id = r.json()["data"]["project"]["ID"]
        return workfront.objects.project.WFProject(self.wf, proj_id)
