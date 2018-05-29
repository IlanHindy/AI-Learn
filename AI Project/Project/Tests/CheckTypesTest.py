from ..Tests.TestBase import TestBase
from ..Utilities.PythonTools import PythonTools


class CheckTypesTest(TestBase, parentWindow):
    """description of class"""

    def __init__(self):
        super(CheckTypesTest, self).__init__(parentWindow)
        self.size = 10
        self.add_test("1 parameter")
        self.add_test(self.check_1_prm_1_option_success)
        self.add_test(self.check_1_prm_1_option_failure)
        self.add_test(self.check_1_prm_3_options_success_1_returned)
        self.add_test(self.check_1_prm_3_options_failure)
        self.add_test("2 parameters")
        self.add_test(self.check_2_prm_1_option_success)
        self.add_test(self.check_2_prm_1_option_failure)
        self.add_test(self.check_2_prm_3_options_success_return_2)
        self.add_test(self.check_2_prm_3_options_failure)
        self.add_test(self.check_2_parameters_3_options_failure_because_of_length)
        self.add_test("Check int float bool combinations")
        self.add_test(self.check_int_acceped_by_int)
        self.add_test(self.check_int_acceped_by_float)
        self.add_test(self.check_bool_not_acceped_by_int)
        self.add_test(self.check_bool_not_acceped_by_float)
        self.add_test(self.check_float_not_acceped_by_int)
        self.add_test("Checks for CheckUniformList method")
        self.add_test(self.check_uniform_list_success)
        self.add_test(self.check_uniform_list_success_2_types)
        self.add_test(self.check_uniform_list_failure_parameter_is_not_list)
        self.add_test(self.check_uniform_list_failure_list_is_empty)
        self.add_test(self.check_uniform_list_failure_1_option)
        self.add_test(self.check_uniform_list_type_failure_2_options)
        self.add_test(self.check_uniform_list_failure_one_of_the_elements_wrong)
        self.options = []

    def check_method(self, expected_selection, check_name, *parameters):
        method_result = True
        method_result_string = ""
        try:
            if len(parameters) == 1:
                self.printErrorMessage = True
                internal_check_name = check_name + " packed test "
                method_result, method_result_string = self.generate_result(expected_selection,
                                                                           self.test_method(parameters[0]),
                                                                           internal_check_name)
                internal_check_name = check_name + " seperated_version "
                result, result_string = self.generate_result(expected_selection,
                                                             self.test_method_1prm(parameters[0]), internal_check_name)
                method_result &= result
                method_result_string += "\n\t" + result_string
                internal_check_name = check_name + " without showing the error "
                self.printErrorMessage = False
                result, result_string = self.generate_result(expected_selection,
                                                             self.test_method(parameters[0]), internal_check_name)
                method_result &= result
                method_result_string += "\n\t" + result_string

            elif len(parameters) == 2:
                self.printErrorMessage = True
                internal_check_name = check_name + " packed test "
                method_result, method_result_string = self.generate_result(expected_selection,
                                                                           self.test_method(
                                                                               parameters[0], parameters[1]),
                                                                           internal_check_name)
                internal_check_name = check_name + " seperated_version "
                result, result_string = self.generate_result(expected_selection,
                                                             self.test_method_2prm(parameters[0], parameters[1]),
                                                             internal_check_name)
                method_result &= result
                method_result_string += "\n\t" + result_string

            elif len(parameters) == 3:
                self.printErrorMessage = True
                internal_check_name = check_name + " packed test "
                method_result, method_result_string = self.generate_result(expected_selection,
                                                                           self.test_method(
                                                                               parameters[0], parameters[1],
                                                                               parameters[2]), internal_check_name)
                internal_check_name = check_name + " seperated_version "
                result, result_string = self.generate_result(expected_selection,
                                                             self.test_method_3prm(parameters[0], parameters[1],
                                                                                   parameters[2]), internal_check_name)
                method_result &= result
                method_result_string += "\n\t" + result_string

            return method_result, method_result_string
        except Exception as e:
            PythonTools.printException("Error in " + check_name)
            return False, internal_check_name + " Failed because of exception : " + e.message

    def generate_result(self, expected_selection, selection, check_name):
        if expected_selection == selection:
            return True, check_name + " OK " + \
                "The selection is :" + str(selection)
        else:
            return False, check_name + " Failed the selection is : " + str(selection) + " instead of : " + str(
                expected_selection)

    def test_method(self, *parameters):
        if len(self.options) == 1:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0])
        elif len(self.options) == 2:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0], self.options[1])
        else:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0], self.options[1],
                                          self.options[2])

    def uniform_list_check_method(self, printErrorMessage, expected_selection, check_name, listPrm, *options):
        try:
            return self.generate_result(expected_selection,
                                        PythonTools.CheckUniformList(check_name, listPrm, printErrorMessage, *options),
                                        check_name)
        except Exception as e:
            PythonTools.printException("Error in " + check_name)
            return False, internal_check_name + " Failed because of exception : " + e.message

    def test_method_1prm(self, prm1):
        if len(self.options) == 1:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0])
        elif len(self.options) == 2:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0], self.options[1])
        else:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0], self.options[1],
                                          self.options[2])

    def test_method_2prm(self, prm1, prm2):
        if len(self.options) == 1:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0])
        elif len(self.options) == 2:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0], self.options[1])
        else:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0], self.options[1],
                                          self.options[2])

    def test_method_3prm(self, prm1, prm2, prm3):
        if len(self.options) == 1:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0])
        elif len(self.options) == 2:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0], self.options[1])
        else:
            return PythonTools.CheckTypes(locals(), self.printErrorMessage, self.options[0], self.options[1],
                                          self.options[2])

    def check_1_prm_1_option_success(self):
        self.options = [int]
        return self.check_method(0, "check_1_prm_1_option_success", 1)

    def check_1_prm_1_option_failure(self):
        self.options = [basestring]
        return self.check_method(-1, "check_1_prm_1_option_failure", 1)

    def check_1_prm_3_options_success_1_returned(self):
        self.options = [basestring, int, bool]
        return self.check_method(1, "check_1_prm_3_options_success_1_returned", 1)

    def check_1_prm_3_options_failure(self):
        self.options = [int, float, bool]
        return self.check_method(-1, "check_1_prm_3_options_failure", "1")

    def check_2_prm_1_option_success(self):
        self.options = [[[int, float], [int, bool]]]
        return self.check_method(0, "check_2_prm_1_option_success", 1.1, False)

    def check_2_prm_1_option_failure(self):
        self.options = [[[int, float], [bool, int]]]
        return self.check_method(-1, "check_2_prm_1_option_failure", 1.1, "False")

    def check_2_prm_3_options_success_return_2(self):
        self.options = [[[int, float], [float, int]], [[str, float], [int, float]], [float, bool]]
        return self.check_method(2, "check_2_prm_3_options_success_return_2", 1.1, False)

    def check_2_prm_3_options_failure(self):
        self.options = [[[int, float], [float, int]], [[str, float], [int, float]], [int, float]]
        return self.check_method(-1, "check_2_prm_3_options_failure", 1.1, False)

    def check_2_parameters_3_options_failure_because_of_length(self):
        self.options = [[[int, float], [float, int], bool], [[str, float]], [int, float, bool]]
        return self.check_method(-1, "check_2_parameters_3_options_failure_because_of_length", 1.1, False)

    def check_int_acceped_by_int(self):
        self.options = [int]
        return self.check_method(0, "check_int_acceped_by_int", 1)

    def check_int_acceped_by_float(self):
        self.options = [float]
        return self.check_method(0, "check_int_acceped_by_float", 1)

    def check_bool_not_acceped_by_int(self):
        self.options = [int]
        return self.check_method(-1, "check_bool_not_acceped_by_int", True)

    def check_bool_not_acceped_by_float(self):
        self.options = [int]
        return self.check_method(-1, "check_bool_not_acceped_by_float", True)

    def check_float_not_acceped_by_int(self):
        self.options = [int]
        return self.check_method(-1, "check_float_not_acceped_by_int", 1.1)

    def check_uniform_list_success(self):
        return self.uniform_list_check_method(True, 0, "check_uniform_list_success", [1, 2, 3, 4, 5, 6], int)

    def check_uniform_list_success_2_types(self):
        return self.uniform_list_check_method(True, 1, "check_uniform_list_success_2_types", [1, 2, 3, 4, 5, 6], bool,
                                              int)

    def check_uniform_list_failure_parameter_is_not_list(self):
        return self.uniform_list_check_method(True, -1, "check_uniform_list_failure_parameter_is_not_list", 1, int)

    def check_uniform_list_failure_list_is_empty(self):
        return self.uniform_list_check_method(True, -1, "check_uniform_list_failure_list_is_empty", [], int)

    def check_uniform_list_type_failure_2_options(self):
        return self.uniform_list_check_method(True, -1, "check_uniform_list_type_failure_2_options", [1, 2, 3, 4, 5],
                                              str, bool)

    def check_uniform_list_failure_1_option(self):
        return self.uniform_list_check_method(True, -1, "check_uniform_list_failure_1_option", [1, 2, 3, 4, 5], bool)

    def check_uniform_list_failure_one_of_the_elements_wrong(self):
        return self.uniform_list_check_method(True, -1, "check_uniform_list_failure_one_of_the_elements_wrong",
                                              [1, True, 2, 3, 4, 5], int)

    def check_uniform_list_failure_one_of_the_elements_wrong(self):
        return self.uniform_list_check_method(False, -1, "check_uniform_list_failure_one_of_the_elements_wrong",
                                              [1, True, 2, 3, 4, 5], int)
