from workfront.exceptions import WFException
import json


class WFObject(object):

    def __init__(self, wf, obj_code, idd):
        self.wf = wf
        self.wf_id = idd
        self.obj_code = obj_code

    def get_fields(self, fields):
        r = self.wf.get_object(self.obj_code, self.wf_id, fields)
        if r.status_code != 200:
            err = "When getting fields for {} {}: {}"
            err = err.format(self.obj_code, self.wf_id, r.json())
            raise WFException(err)
        return r.json()["data"]


class WFParamValuesObject(WFObject):

    def __init__(self, wf, obj_code, idd):
        super(WFParamValuesObject, self).__init__(wf, obj_code, idd)

    def get_param_values(self):
        '''
        @return: A dictionary where each item is:
        - key: parameter name
        - value: value for the parameter
        @warning: Be careful with list fields; workfront returns a single value
        when the list field only contains one value and return a list of values
        when there are more than one field.
        '''
        r = self.wf.get_object(self.obj_code, self.wf_id,
                               ["parameterValues:*"])
        if r.status_code != 200:
            err = "When getting parameter values for {} {}: {}"
            err = err.format(self.obj_code, self.wf_id, r.json())
            raise WFException(err)
        pv = {}
        for key, value in r.json()['data']['parameterValues'].items():
            # parameter names have a "DE:" prefix on each of them, so we need
            # to remove them
            pv[key[3:]] = value
        return pv

    def set_param_values(self, param_value_dict):
        '''
        @summary: Set custom form fields for this object.
        @param param_value_dict: dictionary of custom fields where each item
        is:
        - name of the custom field
        - value of the custom field
        '''
        pv = {}
        for k, v in param_value_dict.items():
            pv["DE:%s" % k] = v

        updates = {"parameterValues": pv}
        params = {"updates": json.dumps(updates)}
        r = self.wf.put_object(self.obj_code, self.wf_id, params)
        if r.status_code != 200:
            err = "When setting parameter values for {} {}: {}"
            err = err.format(self.obj_code, self.wf_id, r.json())
            raise WFException(err)
