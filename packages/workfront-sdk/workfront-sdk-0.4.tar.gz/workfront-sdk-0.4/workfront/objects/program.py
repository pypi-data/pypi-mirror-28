from workfront.objects.codes import WFObjCode
from workfront.exceptions import WFException
from workfront.objects.generic_objects import WFParamValuesObject
import workfront.objects.portfolio


class WFProgram(WFParamValuesObject):

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param idd: worfront id of the program
        '''
        super(WFProgram, self).__init__(wf, WFObjCode.program, idd)

    def get_portfolio(self):
        '''
        @return: the portfolio asociated with this program.
        '''
        r = self.wf.get_object(self.obj_code, self.wf_id, ["portfolio:ID"])
        if r.status_code != 200:
            err = "When getting portfolio from project {}: {}"
            err = err.format(self.wf_id, r.json())
            raise WFException(err)

        proj_id = r.json()["data"]["portfolio"]["ID"]
        return workfront.objects.portfolio.WFPortfolio(self.wf, proj_id)
