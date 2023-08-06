from abc import ABCMeta, abstractproperty

from dataclean.cleaning import (
    OUTLIER_REMOVAL_METHODS,
    NULL_REMOVAL_METHODS,
    TYPE_CONVERT_METHODS
)
from dataclean.codegen import (
    EXPORT_FUNCTION_SIGNATURE,
    STEP_CODE_PREFIX,
    STEP_CODE_SUFFIX
)

class DataCleanStepBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, **params):
        self.params = params
        self.replacement_method = self.params.pop('replacement_method')

    @abstractproperty
    def cleaning_function(self):
        """should return a function that returns a dataframe, decorated
        with the @renderable decorator from dataclean.codegen"""
        pass

    def execute(self, dataframe, allow_inplace = False):
        return self.cleaning_function(
            dataframe if allow_inplace else dataframe.copy(),
            **self.params
        )

    @abstractproperty
    def description(self):
        """should return a description of the step, commas will be
        turned into newlines when viewed in the PipelineItemWidget"""
        pass

    def render_code(self):
        return self.cleaning_function.render_code(**{
            **self.params,
            'code_comment' : self.description
        })

    def required_import_statements(self):
        #will work if the cleaning function is decorated with @renderable
        return self.cleaning_function.get_module_dependencies()

class OutlierRemovalStep(DataCleanStepBase):

    def __init__(self, **params):
        super().__init__(**params)
        self.colname = self.params['colname']
        self.low_cut = self.params['low_cut']
        self.high_cut = self.params['high_cut']

    @property
    def cleaning_function(self):
        return OUTLIER_REMOVAL_METHODS[self.replacement_method]

    @property
    def description(self):
        description = (
            'On {colname}, '
            + 'for values outside {low_cut} to {high_cut}, {replacement_method}'
        ).format(
            colname=self.colname,
            low_cut=self.low_cut,
            high_cut=self.high_cut,
            replacement_method=self.replacement_method.value
        )

        return description

class NullRemovalStep(DataCleanStepBase):

    def __init__(self, **params):
        super().__init__(**params)
        self.colname = self.params['colname']

    @property
    def cleaning_function(self):
        return NULL_REMOVAL_METHODS[self.replacement_method]

    @property
    def description(self):
        description = (
            'On {colname}, '
            + 'for missing values, {replacement_method}'
        ).format(
            colname=self.colname,
            replacement_method=self.replacement_method.value
        )

        return description

class TypeConversionStep(DataCleanStepBase):

    def __init__(self, **params):
        super().__init__(**params)
        self.colname = self.params['colname']
        self.data_type = self.params['data_type']

    @property
    def cleaning_function(self):
        return TYPE_CONVERT_METHODS[self.replacement_method]

    @property
    def description(self):
        description = (
            'On {colname}, '
            + 'for non {data_type} types, {replacement_method}'
        ).format(
            colname=self.colname,
            replacement_method=self.replacement_method.value,
            data_type=self.data_type.__name__
        )

        return description

class Pipeline(object):

    def __init__(self):
        self.steps = []

    def append(self, step):
        self.steps.append(step)

    def remove(self, step):
        self.steps.remove(step)

    def replace(self, old_step, new_step):
        if old_step in self.steps:
            index = self.steps.index(old_step)
            self.steps.remove(old_step)
            self.steps.insert(index, new_step)

    def execute(self, dataframe, up_to_step=None, allow_inplace=False):
        new_dataframe = dataframe
        for step in self.steps:
            if step is up_to_step: break
            new_dataframe = step.execute(new_dataframe, allow_inplace)

        return new_dataframe

    def export(self):

        code = ''
        imports = []

        for step in self.steps:
            code += step.render_code()
            imports += step.required_import_statements()

        export_code = EXPORT_FUNCTION_SIGNATURE

        for import_statement in set(imports):
            export_code += import_statement

        export_code += STEP_CODE_PREFIX + code + STEP_CODE_SUFFIX

        return export_code
