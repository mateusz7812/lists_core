import copy

from TaskProcessor.ProcessorInterface import Processor


class AccountProcessor(Processor):
    name = "account"

    def get_required_requests(self, response):
        if response.request.action == "add":
            return []
        elif response.request.action == "get":
            return []
        elif response.request.action == "del":
            return []

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")

        if not ("login" in data.keys() and "password" in data.keys()):
            response.status = "failed"
            response.result["error"] = "no login/password"
            return response

        if response.request.action == "add" and "id" not in data.keys():
            rows = self.managers[0].manage("get", {})
            if len(rows):
                row = rows[0]
                last_id = row["id"]
            else:
                last_id = 0
            data["id"] = last_id + 1
        response.result["objects"] = self.managers[0].manage(response.request.action, data)
        response.status = "handled"
        return response
