from enum import Enum
from dataclean.codegen import renderable
from sklearn.neighbors import KernelDensity

@renderable
def outlier_removal_mean(dataframe, colname, low_cut, high_cut):

    col = dataframe[colname]
    col_numerics = col.loc[col.apply(lambda x: isinstance(x, (int, float)))]

    dataframe.loc[col.apply(
        lambda x:
            isinstance(x, (int, float))
            and (x < low_cut or x > high_cut)
    ), colname] = col_numerics.mean()

    return dataframe

@renderable
def outlier_removal_median(dataframe, colname, low_cut, high_cut):

    col = dataframe[colname]
    col_numerics = col.loc[col.apply(lambda x: isinstance(x, (int, float)))]

    dataframe.loc[col.apply(
        lambda x:
            isinstance(x, (int, float))
            and (x < low_cut or x > high_cut)
    ), colname] = col_numerics.median()

    return dataframe

@renderable
def outlier_removal_mode_numeric(dataframe, colname, low_cut, high_cut):

    col = dataframe[colname]
    col_numerics = col.loc[col.apply(lambda x: isinstance(x, (int, float)))]

    dataframe.loc[col.apply(
        lambda x:
            isinstance(x, (int, float))
            and (x < low_cut or x > high_cut)
    ), colname] = col_numerics.mode().get(0, None)

    return dataframe

@renderable
def outlier_removal_nearest_cut(dataframe, colname, low_cut, high_cut):

    col = dataframe[colname]

    dataframe.loc[col.apply(
        lambda x:
            isinstance(x, (int, float))
            and x < low_cut
    ), colname] = low_cut

    dataframe.loc[col.apply(
        lambda x:
            isinstance(x, (int, float))
            and x > high_cut
    ), colname] = high_cut

    return dataframe

@renderable
def outlier_removal_drop(dataframe, colname, low_cut, high_cut):

    col = dataframe[colname]

    dataframe = dataframe.loc[col.isnull() | col.apply(
        lambda x:
            not isinstance(x, (int, float))
            or (x >= low_cut and x <= high_cut)
    ), :]

    return dataframe

@renderable
def outlier_removal_sample(dataframe, colname, low_cut, high_cut):

    col = dataframe[colname]

    col_numerics = col.loc[col.notnull() & col.apply(
        lambda x: isinstance(x, (int, float))
    )]

    kde = KernelDensity()
    kde.fit(col_numerics.values.reshape(-1,1))

    is_outlier = col.apply(
        lambda x:
            isinstance(x, (int, float))
            and (x < low_cut or x > high_cut)
    )

    samples = kde.sample(is_outlier.sum())

    dataframe.loc[is_outlier, colname] = samples.flatten()

    return dataframe

@renderable
def null_removal_mean(dataframe, colname):

    col = dataframe[colname]
    col_numerics = col.loc[col.apply(lambda x: isinstance(x, (int, float)))]

    dataframe[colname] = col.fillna(col_numerics.mean())

    return dataframe

@renderable
def null_removal_sample(dataframe, colname):

    col = dataframe[colname]

    col_numerics = col.loc[col.notnull() & col.apply(
        lambda x: isinstance(x, (int, float))
    )]

    kde = KernelDensity()
    kde.fit(col_numerics.values.reshape(-1,1))

    samples = kde.sample(col.isnull().sum())

    dataframe.loc[col.isnull(), colname] = samples.flatten()

    return dataframe

@renderable
def null_removal_median(dataframe, colname):

    col = dataframe[colname]
    col_numerics = col.loc[col.apply(lambda x: isinstance(x, (int, float)))]

    dataframe[colname] = col.fillna(col_numerics.median())

    return dataframe

@renderable
def null_removal_mode(dataframe, colname):

    col = dataframe[colname]

    dataframe[colname] = col.fillna(col.mode().get(0, None))

    return dataframe

@renderable
def null_removal_mode_numeric(dataframe, colname):

    col = dataframe[colname]
    col_numerics = col.loc[col.apply(lambda x: isinstance(x, (int, float)))]

    dataframe[colname] = col.fillna(col_numerics.mode().get(0, None))

    return dataframe

@renderable
def null_removal_drop(dataframe, colname):

    dataframe = dataframe.dropna(subset=[colname])

    return dataframe

@renderable
def type_convert_mean(dataframe, colname, data_type):

    col = dataframe[colname]
    col_numerics = col.loc[col.apply(lambda x: isinstance(x, (int, float)))]

    dataframe.loc[col.notnull() & col.apply(
        lambda x: not isinstance(x, data_type)
    ), colname] = col_numerics.mean()

    return dataframe

@renderable
def type_convert_median(dataframe, colname, data_type):

    col = dataframe[colname]
    col_numerics = col.loc[col.apply(lambda x: isinstance(x, (int, float)))]

    dataframe.loc[col.notnull() & col.apply(
        lambda x: not isinstance(x, data_type)
    ), colname] = col_numerics.median()

    return dataframe

@renderable
def type_convert_mode(dataframe, colname, data_type):

    col = dataframe[colname]
    col_this_type = col.loc[col.apply(lambda x: isinstance(x, data_type))]

    dataframe.loc[col.notnull() & col.apply(
        lambda x: not isinstance(x, data_type)
    ), colname] = col_this_type.mode().get(0, None)

    return dataframe

@renderable
def type_convert_cast(dataframe, colname, data_type):

    def try_cast(x):
        try:
            return data_type(x)
        except ValueError:
            return x

    dataframe[colname] = dataframe[colname].apply(try_cast)

    return dataframe

@renderable
def type_convert_drop(dataframe, colname, data_type):

    col = dataframe[colname]

    dataframe = dataframe.loc[col.isnull() | col.apply(
        lambda x: isinstance(x, data_type)
    ), :]

    return dataframe

@renderable
def type_convert_sample(dataframe, colname, data_type):

    col = dataframe[colname]

    col_numerics = col.loc[col.notnull() & col.apply(
        lambda x: isinstance(x, (int, float))
    )]

    kde = KernelDensity()
    kde.fit(col_numerics.values.reshape(-1,1))

    is_wrong_type = col.apply(lambda x: not isinstance(x, data_type))

    samples = kde.sample(is_wrong_type.sum())

    dataframe.loc[is_wrong_type, colname] = samples.flatten()

    return dataframe

class OutlierRemovalMethod(Enum):
    NONE = 'Do Nothing'
    MEAN = 'Replace with Mean'
    MEDIAN = 'Replace with Median'
    NEAREST_CUT = 'Replace with Nearest Cut'
    MODE_NUMERIC = 'Replace with Mode'
    SAMPLE = 'Sample from Column KDE'
    DROP = 'Drop Rows'

class NullRemovalMethod(Enum):
    NONE = 'Do Nothing'
    MEAN = 'Replace with Mean'
    MEDIAN = 'Replace with Median'
    MODE = 'Replace with Most Common Value'
    MODE_NUMERIC = 'Replace with Mode'
    SAMPLE = 'Sample from Column KDE'
    DROP = 'Drop Rows'

class TypeConvertMethod(Enum):
    NONE = 'Do Nothing'
    CAST = 'Try to Cast'
    MEAN = 'Replace with Mean'
    MEDIAN = 'Replace with Median'
    MODE = 'Replace with Most Common Value'
    SAMPLE = 'Sample from Column KDE'
    DROP = 'Drop Rows'

class CategoricalTypes(Enum):
    CONTINUOUS = 'Numeric'
    CATEGORICAL = 'Categorical'

OUTLIER_REMOVAL_METHODS = {
    OutlierRemovalMethod.MEAN : outlier_removal_mean,
    OutlierRemovalMethod.MEDIAN: outlier_removal_median,
    OutlierRemovalMethod.NEAREST_CUT: outlier_removal_nearest_cut,
    OutlierRemovalMethod.DROP: outlier_removal_drop,
    OutlierRemovalMethod.MODE_NUMERIC: outlier_removal_mode_numeric,
    OutlierRemovalMethod.SAMPLE: outlier_removal_sample,
    OutlierRemovalMethod.NONE: renderable(lambda df, *_, **__: df)
}

NULL_REMOVAL_METHODS = {
    NullRemovalMethod.MEAN : null_removal_mean,
    NullRemovalMethod.MEDIAN: null_removal_median,
    NullRemovalMethod.MODE: null_removal_mode,
    NullRemovalMethod.MODE_NUMERIC: null_removal_mode_numeric,
    NullRemovalMethod.DROP: null_removal_drop,
    NullRemovalMethod.SAMPLE: null_removal_sample,
    NullRemovalMethod.NONE: renderable(lambda df, *_, **__: df)
}

TYPE_CONVERT_METHODS = {
    TypeConvertMethod.MEAN : type_convert_mean,
    TypeConvertMethod.MEDIAN: type_convert_median,
    TypeConvertMethod.MODE: type_convert_mode,
    TypeConvertMethod.DROP: type_convert_drop,
    TypeConvertMethod.CAST: type_convert_cast,
    TypeConvertMethod.SAMPLE: type_convert_sample,
    TypeConvertMethod.NONE: renderable(lambda df, *_, **__: df)
}

ALLOWED_TRANSFORMATIONS = {
    CategoricalTypes.CONTINUOUS : [
        OutlierRemovalMethod.MEAN,
        OutlierRemovalMethod.MEDIAN,
        OutlierRemovalMethod.NEAREST_CUT,
        OutlierRemovalMethod.DROP,
        OutlierRemovalMethod.MODE_NUMERIC,
        OutlierRemovalMethod.SAMPLE,
        OutlierRemovalMethod.NONE,
        NullRemovalMethod.MEAN,
        NullRemovalMethod.MEDIAN,
        NullRemovalMethod.MODE_NUMERIC,
        NullRemovalMethod.DROP,
        NullRemovalMethod.SAMPLE,
        NullRemovalMethod.NONE,
        TypeConvertMethod.MEAN,
        TypeConvertMethod.MEDIAN,
        TypeConvertMethod.MODE,
        TypeConvertMethod.DROP,
        TypeConvertMethod.CAST,
        TypeConvertMethod.SAMPLE,
        TypeConvertMethod.NONE
    ],
    CategoricalTypes.CATEGORICAL : [
        NullRemovalMethod.MODE,
        NullRemovalMethod.DROP,
        NullRemovalMethod.NONE,
        TypeConvertMethod.DROP,
        TypeConvertMethod.CAST,
        TypeConvertMethod.MODE,
        TypeConvertMethod.NONE
    ]
}