# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.materialpackagemakers.MaterialPackageMaker \
    import MaterialPackageMaker


class FunctionInputMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS VARIABLES ###

    should_have_user_input_module = True
    user_input_demo_values = []
    user_input_module_import_statements = []
    user_input_tests = []
