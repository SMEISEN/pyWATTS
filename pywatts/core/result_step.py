from typing import Optional, Dict

import pandas as pd

from pywatts.core.base_step import BaseStep
from pywatts.core.filemanager import FileManager


class ResultStep(BaseStep):
    """
    This steps fetch the correct column if the previous step provides data with multiple columns as output
    """

    def __init__(self, input_steps, buffer_element: str):
        super().__init__(input_steps=input_steps)
        self.buffer_element = buffer_element

    def get_result(self, start: pd.Timestamp, end: Optional[pd.Timestamp], buffer_element: str = None,
                   return_all=False, minimum_data=(0, pd.Timedelta(0)), use_result_buffer=False):
        """
        Returns the specified result of the previous step.
        """
        # There exist only one input step in a result buffer
        input_step = list(self.input_steps.values())[0]
        if not return_all:
            return input_step.get_result(start, end, self.buffer_element, minimum_data=minimum_data,
                                         use_result_buffer=use_result_buffer)
        else:
            return {self.buffer_element: input_step.get_result(start, end, self.buffer_element,
                                                               minimum_data=minimum_data,
                                                               use_result_buffer=use_result_buffer)}

    def get_json(self, fm: FileManager) -> Dict:
        """
        Returns all information for restoring the resultStep.
        """
        json_dict = super().get_json(fm)
        json_dict["buffer_element"] = self.buffer_element
        return json_dict

    @classmethod
    def load(cls, stored_step: dict, inputs, targets, module, file_manager):
        """
        Load a stored ResultStep.

        :param stored_step: Informations about the stored step
        :param inputs: The input step of the stored step
        :param targets: The target step of the stored step
        :param module: The module wrapped by this step
        :return: Step
        """
        step = cls(inputs, stored_step["buffer_element"])
        step.id = stored_step["id"]
        step.name = stored_step["name"]
        step.last = stored_step["last"]
        return step


    def further_elements(self, counter: pd.Timestamp) -> bool:
        for input_step in self.input_steps.values():
            if not input_step.further_elements(counter):
                return False
        return True