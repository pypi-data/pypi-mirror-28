from __future__ import division
from abc import ABCMeta, abstractmethod

from IPython.display import display
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import ipywidgets as widgets

from dataclean.cleaning import (
    OutlierRemovalMethod,
    NullRemovalMethod,
    CategoricalTypes,
    TypeConvertMethod,
    ALLOWED_TRANSFORMATIONS
)
from dataclean.pipeline import (
    OutlierRemovalStep,
    NullRemovalStep,
    TypeConversionStep
)

class CallbackManager(object):

    def __init__(self):
        self.callbacks = []

    def send_callbacks(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(*args, **kwargs)

    def register_callback(self, callback):
        self.callbacks.append(callback)

class StepCreatorWidgetControllerBase(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.update_step_callback = CallbackManager()

    def load_data(self, column, numerical_data):
        self.column = column
        self.colname = column.name
        self.numerical_data = numerical_data

    @abstractmethod
    def create_widgets(self, submit_button):
        """create your control widgets, incorporating submit_button to add it
        to the pipeline """
        pass

    @abstractmethod
    def reset_controls(self, categorical_type):
        """reset the controls to their base state"""
        pass

    @abstractmethod
    def update_step(self):
        """send a step back to the column widget"""
        pass

    @abstractmethod
    def render_widget(self, step = None):
        """return the overall parent widget for your controls"""
        pass

class NullReplaceWidgetController(StepCreatorWidgetControllerBase):

    def __init__(self):
        super().__init__()
        self.tab_title = 'Nulls'
        self.transform_type = NullRemovalMethod

    def create_widgets(self, submit_button):
        self.submit_button = submit_button

        self.null_percent_bar = widgets.FloatProgress(
            value=0,
            min=0,
            max=100,
            description='Missing:',
            disabled=False,
            continuous_update=False,
            readout=True,
            readout_format='.2g',
            layout=widgets.Layout(width='400px'),
            bar_style='warning'
        )

        self.null_replace_selector = widgets.Dropdown(
            options=[],
            description='Replacement Method: ',
            layout=widgets.Layout(width='400px'),
            style = {'description_width': 'initial'}
        )
        self.null_replace_selector.observe(self.update_step, names='value')

        self.null_text = widgets.Label()

        self.null_removal_controls = widgets.VBox(
            [
                self.null_text,
                self.null_percent_bar,
                self.null_replace_selector,
                self.submit_button
            ],
            layout=widgets.Layout(width='100%')
        )
        self.null_removal_controls.layout.align_items = 'center'

    def reset_controls(self, categorical_type):

        self.null_replace_selector.unobserve(self.update_step, names='value')

        self.null_text.value = "{0} of {1} ({2:.0f}%) selected".format(
            self.column.isnull().sum(),
            len(self.column),
            100*self.column.isnull().sum()/len(self.column)
        )

        self.null_percent_bar.bar_style = 'warning'
        self.null_percent_bar.value = 100*self.column.isnull().sum()/len(self.column)

        allowed_transforms = {x.value: x for x in ALLOWED_TRANSFORMATIONS[categorical_type] if type(x) is self.transform_type}

        self.null_replace_selector.options = allowed_transforms

        if len(allowed_transforms) > 0:
            self.null_replace_selector.value = self.transform_type.NONE
        self.null_replace_selector.observe(self.update_step, names='value')

    def update_step(self, _ = None):

        if self.null_replace_selector.value == self.transform_type.NONE:
            self.submit_button.disabled = True
            self.null_percent_bar.bar_style = 'warning'
        else:
            self.submit_button.disabled = False
            self.null_percent_bar.bar_style = 'success'

        step = NullRemovalStep(
                replacement_method=self.null_replace_selector.value,
                colname=self.colname
            )

        self.update_step_callback.send_callbacks(step)

    def render_widget(self, step=None):
        if step:
            self.null_replace_selector.value = step.replacement_method
        return self.null_removal_controls

class OutlierReplaceWidgetController(StepCreatorWidgetControllerBase):

    def __init__(self):
        super().__init__()
        self.tab_title = 'Outliers'
        self.transform_type = OutlierRemovalMethod

    def create_widgets(self, submit_button):
        self.submit_button = submit_button
        self.outlier_range_slider = widgets.FloatRangeSlider(
            value=[0, 1],
            min=0,
            max=1,
            step=0.04,
            description='Range:',
            disabled=False,
            continuous_update=False,
            readout=True,
            readout_format='.2g',
            layout=widgets.Layout(width='400px'),
            style={'handle_color' : 'lightblue'}
        )

        self.outlier_replace_selector = widgets.Dropdown(
            options=[],
            description='Replacement Method: ',
            layout=widgets.Layout(width='400px'),
            style = {'description_width': 'initial'}
        )

        self.outlier_range_slider.observe(self.update_step, names='value')
        self.outlier_replace_selector.observe(self.update_step, names='value')
        self.cut_text = widgets.Label()

        self.outlier_removal_controls = widgets.VBox(
            [
                self.cut_text,
                self.outlier_range_slider,
                self.outlier_replace_selector,
                self.submit_button
            ],
            layout=widgets.Layout(width='100%')
        )
        self.outlier_removal_controls.layout.align_items = 'center'

    def reset_controls(self, categorical_type):

        self.outlier_range_slider.unobserve(self.update_step, names='value')
        self.outlier_replace_selector.unobserve(self.update_step, names='value')

        self.cut_text.value = "{0} of {1} ({2:.0f}%) selected".format(
            0,
            len(self.column),
            0.0
        )

        with self.outlier_range_slider.hold_trait_notifications():
            self.outlier_range_slider.min = self.numerical_data.min()
            self.outlier_range_slider.max = self.numerical_data.max()

        self.outlier_range_slider.value=[
            self.numerical_data.min(),
            self.numerical_data.max()
        ]

        allowed_transforms = {x.value: x for x in ALLOWED_TRANSFORMATIONS[categorical_type] if type(x) is self.transform_type}

        self.outlier_replace_selector.options = allowed_transforms

        if len(allowed_transforms) > 0:
            self.outlier_replace_selector.value = self.transform_type.NONE

        self.outlier_range_slider.observe(self.update_step, names='value')
        self.outlier_replace_selector.observe(self.update_step, names='value')

    def update_step(self, _ = None):

        if self.outlier_replace_selector.value == self.transform_type.NONE:
            self.submit_button.disabled = True
        else:
            self.submit_button.disabled = False

        num_values_cut = self.numerical_data[
            (self.numerical_data < self.outlier_range_slider.value[0]) |
            (self.numerical_data > self.outlier_range_slider.value[1])
        ].count()

        percent_values_cut = (
            100 * num_values_cut /
            float(len(self.column))
        )

        self.cut_text.value = "{0} of {1} ({2:.0f}%) selected".format(
            num_values_cut,
            len(self.column),
            percent_values_cut
        )

        step = OutlierRemovalStep(
                replacement_method=self.outlier_replace_selector.value,
                colname=self.colname,
                low_cut=self.outlier_range_slider.value[0],
                high_cut=self.outlier_range_slider.value[1]
            )

        self.update_step_callback.send_callbacks(step)

    def render_widget(self, step = None):
        if step:
            self.outlier_range_slider.value = [step.low_cut, step.high_cut]
            self.outlier_replace_selector.value = step.replacement_method
        return self.outlier_removal_controls

class TypeConvertWidgetController(StepCreatorWidgetControllerBase):

    def __init__(self):
        super().__init__()
        self.transform_type = TypeConvertMethod
        self.tab_title = 'Mismatched Types'

    def load_data(self, column, numerical_data):
        super().load_data(column, numerical_data)
        self.type_count_dict = {float:0, int:0, str:0}

        for data_type, count in self.column.dropna().apply(type).value_counts().iteritems():
            self.type_count_dict[data_type] = count

    def create_widgets(self, submit_button):
        self.submit_button = submit_button

        self.float_percent_bar = widgets.FloatProgress(
            value=0,
            min=0,
            max=100,
            description='Floats:',
            orientation='horizontal'
        )
        self.n_float = widgets.Label()
        float_bar_widget = widgets.HBox([self.float_percent_bar, self.n_float])

        self.int_percent_bar = widgets.FloatProgress(
            value=0,
            min=0,
            max=100,
            description='Ints:',
            orientation='horizontal'
        )
        self.n_int = widgets.Label()
        int_bar_widget = widgets.HBox([self.int_percent_bar, self.n_int])

        self.str_percent_bar = widgets.FloatProgress(
            value=0,
            min=0,
            max=100,
            description='Strings:',
            orientation='horizontal'
        )
        self.n_str = widgets.Label()
        str_bar_widget = widgets.HBox([self.str_percent_bar, self.n_str])

        self.type_selector = widgets.Dropdown(
            options={'int':int, 'float':float, 'string':str},
            description='This column is of type:',
            layout=widgets.Layout(width='300px'),
            style = {'description_width': 'initial'}
        )

        self.replace_selector = widgets.Dropdown(
            description='For mismatched values:',
            layout=widgets.Layout(width='300px'),
            style = {'description_width': 'initial'}
        )

        self.type_selector.observe(self.update_step, names='value')
        self.replace_selector.observe(self.update_step, names='value')

        self.widget = widgets.VBox([
            float_bar_widget,
            int_bar_widget,
            str_bar_widget,
            widgets.HBox([
                widgets.VBox([
                    self.type_selector,
                    self.replace_selector
                ]),
                submit_button
            ])
        ])

        self.bar_widget_dict = {
            float: float_bar_widget,
            int: int_bar_widget,
            str: str_bar_widget
        }

    def reset_controls(self, categorical_type):
        self.type_selector.unobserve(self.update_step, names='value')
        self.replace_selector.unobserve(self.update_step, names='value')

        allowed_transforms = {x.value: x for x in ALLOWED_TRANSFORMATIONS[categorical_type] if isinstance(x, self.transform_type)}

        self.replace_selector.options = allowed_transforms

        if len(allowed_transforms) > 0:
            self.replace_selector.value = self.transform_type.NONE

        current_type = sorted(self.type_count_dict, key=self.type_count_dict.get)[-1]
        if current_type is str and categorical_type is CategoricalTypes.CONTINUOUS:
            current_type = sorted(self.type_count_dict, key=self.type_count_dict.get)[-2]

        self.type_selector.value = current_type

        for dtype, widget_box in self.bar_widget_dict.items():
            widget_box.children[0].value = 100*self.type_count_dict[dtype]/len(self.column)
            widget_box.children[0].bar_style = 'success' if current_type is dtype else 'warning'
            widget_box.children[1].value = '{0} of {1} ({2:.0f}%)'.format(
                self.type_count_dict[dtype],
                len(self.column),
                widget_box.children[0].value
            )

        self.type_selector.observe(self.update_step, names='value')
        self.replace_selector.observe(self.update_step, names='value')

    def update_step(self, _ = None):
        for dtype, widget_box in self.bar_widget_dict.items():
            widget_box.children[0].bar_style = 'success' if self.type_selector.value is dtype else 'warning'

        if self.replace_selector.value == self.transform_type.NONE:
            self.submit_button.disabled = True
        else:
            self.submit_button.disabled = False

        step = TypeConversionStep(
                replacement_method=self.replace_selector.value,
                colname=self.colname,
                data_type=self.type_selector.value
            )
        self.update_step_callback.send_callbacks(step)

    def render_widget(self, step = None):
        if step:
            self.type_selector.value = step.data_type
            self.replace_selector.value = step.replacement_method
        return self.widget

class PlotWidgetController(object):

    gs_one_plot = gridspec.GridSpec(1,1)
    gs_two_plots = gridspec.GridSpec(2, 1, height_ratios = [1,1], hspace = 0.1)

    CUT_LINE_COLOUR = 'red'
    FULLY_CUT_COLOUR = 'orange'

    def __init__(self):
        self.output_widget = widgets.Output(
            layout = widgets.Layout(
                min_width='300px',
                height='160px'
            )
        )
        self.create_figure()

    def load_data(self, column, numerical_data):
        self.column = column
        self.colname = column.name
        self.numerical_data = numerical_data

    def create_figure(self):
        with plt.style.context('seaborn'):
            self.fig = plt.figure()
            self.ax_main = self.fig.add_subplot(self.gs_two_plots[0])

            self.ax_mod = self.fig.add_subplot(
                self.gs_two_plots[1]
            )
            
            plt.setp(self.ax_mod.get_xticklabels(), visible = False)
            plt.setp(self.ax_mod.get_yticklabels(), visible = False)

            self.ax_cut = self.ax_main.twinx()

            #enforce desired draw order
            self.ax_mod.set_zorder(1)
            self.ax_main.set_zorder(2)
            self.ax_cut.set_zorder(3)

            self.ax_cut.get_xaxis().set_visible(False)
            self.ax_cut.get_yaxis().set_visible(False)

            self.ax_main.tick_params(axis='y', which='major', labelsize=12)
            self.ax_mod.tick_params(axis='y', which='major', labelsize=12)

    def display_figure(self):
        self.output_widget.clear_output(wait=True)

        fig_width = 0.1*len(self.ax_main.get_xticks())+3.5
        fig_height = 2.4
        self.fig.set_size_inches(fig_width, fig_height)

        self.output_widget.layout.width = '{}px'.format(fig_width*70)
        self.output_widget.layout.height = '{}px'.format(fig_height*80)

        with self.output_widget:
            display(self.fig)

    def reset_plots(self, categorical_type):
        if self.fig:
            plt.close(self.fig)
        self.create_figure()

        self.categorical_type = categorical_type
        self.draw_main_plot()
        self.update_plots()

    def draw_main_plot(self):
        with plt.style.context('seaborn'):
            self.ax_main.cla()
            self.ax_mod.cla()

            if self.categorical_type is CategoricalTypes.CATEGORICAL:
                col = self.column.dropna().value_counts()
                col.index = col.index.format()
                col.sort_index().plot(
                    kind='bar',
                    ax=self.ax_main,
                    alpha=0.4
                )
            else:
                hist_orig, self.bins = np.histogram(self.numerical_data)
                self.bin_width = self.bins[1]-self.bins[0]

                self.ax_main.bar(
                    self.bins[:-1],
                    hist_orig,
                    width=self.bin_width,
                    align='edge',
                    alpha=0.4
                 )

            self.ymax = self.ax_main.get_ylim()[1]
            self.low_cut_line, = self.ax_main.plot(
                [None, None],
                [self.ymax, 0],
                color=self.CUT_LINE_COLOUR,
            )

            self.high_cut_line, = self.ax_main.plot(
                [None, None],
                [self.ymax, 0],
                color=self.CUT_LINE_COLOUR,
            )

    def update_plots(self, step = None, col_mod = None):

        if isinstance(step, OutlierRemovalStep):
            self.low_cut_line.set_xdata([[step.low_cut, step.low_cut]])
            self.high_cut_line.set_xdata([[step.high_cut, step.high_cut]])

            self.draw_cut_plot(step.low_cut, step.high_cut)
        else:
            self.hide_cut_plot()

        self.draw_modified_plot(col_mod if col_mod is not None else self.column)
        self.display_figure()

    def draw_modified_plot(self, col_mod):
        with plt.style.context('seaborn'):
            self.ax_mod.clear()

            data_mod = col_mod.loc[col_mod.apply(
                lambda x:
                    isinstance(x, (int, float))
            )]
            data_mod = data_mod.dropna()
            col_mod = col_mod.dropna().value_counts()

            if (
                self.categorical_type is CategoricalTypes.CATEGORICAL
                and not self.column.dropna().value_counts().equals(col_mod)
            ):
                self.ax_main.set_position(self.gs_two_plots[0].get_position(self.fig))
                self.ax_cut.set_position(self.gs_two_plots[0].get_position(self.fig))

                plt.setp(self.ax_main.get_xticklabels(), visible = False)
                plt.setp(self.ax_mod.get_xticklabels(), visible = True)
                plt.setp(self.ax_mod.get_yticklabels(), visible = True)

                col_orig = self.column.dropna().value_counts()

                col_mod.index = col_mod.index.format()
                col_orig.index = col_orig.index.format()

                col_delta = col_mod.sub(col_orig, fill_value=0)
                col_delta = col_delta[col_delta>0]

                col_mod = col_mod.sub(col_delta, fill_value=0)

                col_mod = pd.concat([col_mod, col_delta], axis=1)

                col_mod.sort_index().plot(
                    kind='bar',
                    ax=self.ax_mod,
                    alpha=0.4,
                    stacked=True,
                    legend=False
                )

            elif (
                self.categorical_type is not CategoricalTypes.CATEGORICAL
                and not data_mod.equals(self.numerical_data)
            ):
                self.ax_main.set_position(self.gs_two_plots[0].get_position(self.fig))
                self.ax_cut.set_position(self.gs_two_plots[0].get_position(self.fig))

                plt.setp(self.ax_main.get_xticklabels(), visible = False)
                plt.setp(self.ax_mod.get_xticklabels(), visible = True)
                plt.setp(self.ax_mod.get_yticklabels(), visible = True)

                hist_mod, _ = np.histogram(data_mod, self.bins)
                hist_orig, _ = np.histogram(self.numerical_data, self.bins)

                hist_delta = hist_mod - hist_orig
                hist_delta[hist_delta < 0] = 0

                self.ax_mod.bar(
                    self.bins[:-1],
                    hist_mod-hist_delta,
                    width=self.bin_width,
                    align='edge',
                    alpha=0.4
                )
                self.ax_mod.bar(
                    self.bins[:-1],
                    hist_delta,
                    width=self.bin_width,
                    color='g',
                    bottom=hist_mod-hist_delta,
                    align='edge',
                    alpha=0.4
                )
            else:
                self.ax_main.set_position(self.gs_one_plot[0].get_position(self.fig))
                self.ax_cut.set_position(self.gs_one_plot[0].get_position(self.fig))
                plt.setp(self.ax_main.get_xticklabels(), visible = True)
                plt.setp(self.ax_mod.get_xticklabels(), visible = False)
                plt.setp(self.ax_mod.get_yticklabels(), visible = False)

    def draw_cut_plot(self, low_cut, high_cut):
        with plt.style.context('seaborn'):
            self.ax_cut.set_visible(True)

            ticks = self.ax_cut.get_xticks()
            self.ax_cut.clear()
            self.ax_cut.set_xticks(ticks)

            cut_data = self.numerical_data.loc[self.numerical_data.apply(
                lambda x:
                    x < low_cut or
                    x > high_cut
            )]

            hist_cut, _ = np.histogram(cut_data, self.bins)

            self.ax_cut.bar(
                self.bins[:-1],
                hist_cut,
                width=self.bin_width,
                align='edge',
                color=self.FULLY_CUT_COLOUR,
                alpha=0.4
            )

            self.ax_cut.set_ylim(self.ax_main.get_ylim())

    def hide_cut_plot(self):
        self.low_cut_line.set_xdata([[None, None]])
        self.high_cut_line.set_xdata([[None, None]])
        self.ax_cut.set_visible(False)

    def render_widget(self):
        if self.fig:
            plt.close(self.fig)
        self.create_figure()
        return self.output_widget

class ColumnWidgetController(object):

    STRING_THRESHOLD = 0.8

    def __init__(self):

        self.widget = None
        self.step_being_modified = None
        self.new_step_callback = CallbackManager()
        self.modify_step_callback = CallbackManager()
        self.active_callback = self.new_step_callback
        self.categorical_type = None

        self.plot_widget_controller = PlotWidgetController()

        def update_active_step(new_step):
            self.active_step = new_step
            col_mod = new_step.execute(self.dataframe)[self.colname]
            self.redraw_preview(col_mod)
            self.plot_widget_controller.update_plots(new_step, col_mod)

        self.step_creation_controls = [
            NullReplaceWidgetController(),
            OutlierReplaceWidgetController(),
            TypeConvertWidgetController()
        ]

        self.controls_dict = {}

        for controller in self.step_creation_controls:
            self.controls_dict[controller.transform_type] = controller
            controller.update_step_callback.register_callback(update_active_step)

        self.create_widgets()

    def create_widgets(self):

        self.categorical_selector = widgets.Dropdown(
            options={cat_type.value: cat_type for cat_type in CategoricalTypes},
            layout=widgets.Layout(width='80%')
        )

        self.submit_button = widgets.Button(
            description = 'Add to Pipeline'
        )

        self.plot_widget_container = widgets.VBox(
            [
                self.plot_widget_controller.render_widget(),
                self.categorical_selector
            ],
            layout=widgets.Layout(
                width='350px',
                height='220px',
                overflow_x='scroll',
                overflow_y='auto'
            )
        )

        self.plot_widget_container.layout.align_items = 'flex-start'

        self.categorical_selector.observe(self.categorical_selector_onchange, names='value')

        self.submit_button.on_click(self.submit_button_clicked)

        self.preview_widget = widgets.HTML()
        self.preview_widget_container = widgets.VBox([
            widgets.Label(value='Current Step'),
            self.preview_widget
        ], layout=widgets.Layout(max_height='200px'))

        self.tab_widget = widgets.Tab(
            layout=widgets.Layout(
                overflow_x='scroll',
                width='600px',
                height='90%'
            )
        )

        self.tab_widget.observe(self.tab_widget_onchange, names='selected_index')

        for controller in self.step_creation_controls:
            controller.create_widgets(self.submit_button)

        self.widget = widgets.HBox(
            [self.plot_widget_container, self.tab_widget, self.preview_widget_container],
            layout=widgets.Layout(
                display='flex',
                align_items='stretch',
                width='100%',
                height='220px'
            )
        )

    def tab_widget_onchange(self, _):
        index = self.tab_widget.selected_index

        for controller in self.controls_dict.values():
            if controller.tab_title == self.tab_widget.get_title(index):
                controller.update_step()

    def categorical_selector_onchange(self, _):
        self.categorical_type = self.categorical_selector.value

        self.active_step = NullRemovalStep(
            replacement_method=NullRemovalMethod.NONE,
            colname=self.colname
        )

        self.reset_controls()

    def submit_button_clicked(self, _):
        self.active_callback.send_callbacks(self.active_step)

    def load_data(self, series, dataframe, step = None):
        self.dataframe = dataframe
        self.column = series
        self.colname = series.name

        type_count_dict = {float:0, int:0, str:0}

        for data_type, count in series.dropna().apply(type).value_counts().iteritems():
            type_count_dict[data_type] = count

        if not self.categorical_type:
            self.categorical_type = CategoricalTypes.CONTINUOUS

            if (type_count_dict[str] >= self.STRING_THRESHOLD*(
                type_count_dict[str]
                + type_count_dict[int]
                + type_count_dict[float]
            )):
                self.categorical_type = CategoricalTypes.CATEGORICAL

        self.numerical_data = series.loc[series.apply(
            lambda x:
                isinstance(x, (int, float))
        )]

        self.numerical_data = self.numerical_data.dropna()

        for controller in self.step_creation_controls:
            controller.load_data(
                column = self.column,
                numerical_data = self.numerical_data
            )
        self.plot_widget_controller.load_data(
                column = self.column,
                numerical_data = self.numerical_data
            )

        self.redraw_preview()
        self.step_being_modified = step

    def redraw_preview(self, col_modified = None):

        if col_modified is not None:
            col_mod = col_modified.reindex(
                index = self.column.index,
                fill_value='<br>'
            )
        else:
            col_mod = self.column

        self.preview_widget.value = '<center>This Step</center>' + pd.concat(
            [self.column.rename('before'), col_mod.rename('after')],
            axis=1
        ).style.set_table_attributes('class="table"').render()

    def render_widget(self):
        self.reset_controls()
        self.redraw_preview()
        if self.step_being_modified:
            self.set_controls_for_step(self.step_being_modified)
        return self.widget

    def reset_controls(self):
        self.tab_widget.unobserve(self.tab_widget_onchange, names='selected_index')
        self.categorical_selector.unobserve(self.categorical_selector_onchange, names='value')

        self.submit_button.description = 'Add to Pipeline'
        self.active_callback = self.new_step_callback

        tab_children = []
        tab_titles = []

        for transform_type in set(
            type(transform) for transform in ALLOWED_TRANSFORMATIONS[self.categorical_type]
        ):
            tab_children.append(
                self.controls_dict[transform_type].render_widget()
            )
            tab_titles.append(
                self.controls_dict[transform_type].tab_title
            )

        self.tab_widget.children = tuple(tab_children)

        for i in range(len(tab_children)):
            self.tab_widget.set_title(i, tab_titles[i])

        self.tab_widget.selected_index = 0

        self.active_step = NullRemovalStep(
            replacement_method=NullRemovalMethod.NONE,
            colname=self.colname
        )

        for controller in self.step_creation_controls:
            controller.reset_controls(
                categorical_type = self.categorical_type
            )

        self.submit_button.disabled = True

        self.categorical_selector.disabled = False
        self.categorical_selector.value = self.categorical_type

        self.plot_widget_controller.reset_plots(
            self.categorical_type
        )

        self.tab_widget.observe(self.tab_widget_onchange, names='selected_index')
        self.categorical_selector.observe(self.categorical_selector_onchange, names='value')

    def set_controls_for_step(self, step):

        if hasattr(step, 'colname') and step.colname == self.colname:

            while step.replacement_method not in ALLOWED_TRANSFORMATIONS[self.categorical_type]:
                self.categorical_selector.index = (
                    self.categorical_selector.index + 1
                ) % len(self.categorical_selector.options)

            self.tab_widget.children = [
                self.controls_dict[
                    type(step.replacement_method)
                ].render_widget(step)
            ]

            self.submit_button.description = 'Replace Current Step'
            self.active_callback = self.modify_step_callback
            self.tab_widget.set_title(0, 'Modifying Current Step')
            self.tab_widget.selected_index = 0
        else:
            inactive_text = (
                'Currently modifying another step. '
                'Open the {} widget to modify it or '
                'click the "+" button on the pipeline widget to add a new one.'
            ).format(step.colname if hasattr(step, 'colname') else 'dataframe')

            self.tab_widget.children = [widgets.Textarea(
                value=inactive_text,
                disabled=True,
                layout=widgets.Layout(width='100%')
            )]

            self.tab_widget.set_title(0, self.colname)
        self.categorical_selector.disabled = True

class DataFrameWidgetController(object):

    def __init__(self, pipeline_widget, sampled_rows):
        self.resample_callback = CallbackManager()

        self.pipeline_widget_container = widgets.Accordion(children=[pipeline_widget])
        self.pipeline_widget_container.set_title(0, "Pipeline")
        self.pipeline_widget_container.selected_index = None
        self.preview_widget = widgets.Output(
            layout=widgets.Layout(
                    overflow_y='scroll',
                    overflow_x='scroll',
                    width='100%',
                    height='190px'
            )
        )
        self.preview_widget_container = widgets.Accordion(children=[self.preview_widget])
        self.preview_widget_container.set_title(0,"DataFrame Preview")
        self.preview_widget_container.selected_index = None
        child_widgets = [self.preview_widget_container, self.pipeline_widget_container]

        if sampled_rows:
            sample_label = widgets.Label(
                value='Viewing a sample of {} rows from your dataframe.'.format(sampled_rows)
            )
            sample_btn = widgets.Button(description='Resample')
            sample_btn.on_click(lambda _: self.resample_callback.send_callbacks())
            child_widgets = [widgets.HBox([sample_label, sample_btn])] + child_widgets

        self.widget = widgets.VBox(child_widgets)

    def redraw_preview(self, dataframe):
        self.preview_widget.clear_output(wait=True)
        with self.preview_widget:
            display(dataframe.style.set_caption(
               'Preview up to the current pipeline step'
            ))

    def render_widget(self, dataframe):
        self.redraw_preview(dataframe)
        return self.widget

    def display_pipeline(self):
        self.pipeline_widget_container.selected_index = 0

class PipelineWidgetController(object):

    CAROUSEL_LAYOUT = widgets.Layout(
                    overflow_x='scroll',
                    width='800px',
                    height='',
                    flex_direction='row',
                    display='flex'
                )

    def __init__(self, pipeline):

        self.pipeline = pipeline
        self.pipeline_view = widgets.Box(children = [], layout = self.CAROUSEL_LAYOUT)
        self.info_label = widgets.Label(value='')
        self.info_label.layout.height = '30px'

        self.add_button = widgets.Button(description = '+')
        self.add_button.layout.visibility = 'hidden'
        self.add_button.on_click(lambda _: self._enter_add_mode())

        self.add_mode_callback = CallbackManager()
        self.edit_mode_callback = CallbackManager()
        self.delete_step_callback = CallbackManager()
        self.execute_callback = CallbackManager()
        self.export_callback = CallbackManager()

        self.execute_button = widgets.Button(description = 'Execute Pipeline')
        self.execute_button.on_click(lambda _: self._execute_pipeline())

        self.export_button = widgets.Button(description = 'Export to Code')
        self.export_button.on_click(lambda _:self._export_pipeline())

    def render_widget(self, active_step = None):

        children=[]
        self.pipeline_items = []
        self.info_label.value = 'Add a step to get started'

        for step in self.pipeline.steps:
            pipeline_item = PipelineStepWidgetController(step)

            pipeline_item.modify_step_callback.register_callback(
                self._enter_edit_mode
            )

            pipeline_item.delete_step_callback.register_callback(
                self._delete_step
            )

            self.pipeline_items.append(pipeline_item)
            children.append(pipeline_item.widget)

        if children:
            children.append(
                widgets.VBox([
                    self.add_button,
                    self.execute_button,
                    self.export_button
                ],
                layout = widgets.Layout(min_width = '150px'))
            )
            self.info_label.value = ''

        self.pipeline_view.children = tuple(children)
        self.widget = widgets.VBox([self.pipeline_view, self.info_label])
        self._enter_edit_mode(active_step)

        return self.widget

    def _enter_edit_mode(self, step):
        if step is not None:
            self.add_button.layout.visibility = None
            for pipeline_item in self.pipeline_items:
                if pipeline_item.step is step:
                    pipeline_item.set_active_style()
                else:
                    pipeline_item.set_inactive_style()
            self.edit_mode_callback.send_callbacks(step)
            message = 'Modifying step'
            if hasattr(step, 'colname'): message += ' on column ' + step.colname
            self.display_message(message)

    def _export_pipeline(self):
        self.export_callback.send_callbacks()

    def _execute_pipeline(self):
        self.execute_callback.send_callbacks()

    def _delete_step(self, step):
        self.add_button.layout.visibility = 'hidden'
        self.delete_step_callback.send_callbacks(step)

    def _enter_add_mode(self):
        self.add_button.layout.visibility = 'hidden'
        for pipeline_item in self.pipeline_items:
            pipeline_item.set_inactive_style()
        self.add_mode_callback.send_callbacks()
        self.display_message('')

    def display_message(self, message):
        self.info_label.value = message

class PipelineStepWidgetController(object):

    def __init__(self, step):

        self.select_box = widgets.Select(
            options = step.description.replace(', ','\n').splitlines(),
            rows = 3,
            disabled = False,
            layout = widgets.Layout(width='200px')
        )

        self.modify_button = widgets.Button(
            layout = widgets.Layout(height='25px', width='98%')
        )

        self.delete_button = widgets.Button(
            disbaled = True,
            layout = widgets.Layout(height='25px', width='98%')
        )

        self.widget = widgets.VBox(
            [
                self.modify_button,
                self.select_box,
                self.delete_button
            ],
            layout = widgets.Layout(min_width='200px')
        )

        self.step = step
        self.modify_step_callback = CallbackManager()
        self.delete_step_callback = CallbackManager()

        self.modify_button.on_click(self.modify_button_on_click)
        self.delete_button.on_click(self.delete_button_on_click)

        self.set_inactive_style()

    def modify_button_on_click(self, _):
        self.modify_step_callback.send_callbacks(self.step)

    def delete_button_on_click(self, _):
        self.delete_step_callback.send_callbacks(self.step)

    def set_active_style(self):
        self.modify_button.button_style = 'primary'
        self.modify_button.description = 'Modifying'
        self.delete_button.disabled = False
        self.delete_button.description = 'Delete Step'
        self.delete_button.button_style = 'warning'

    def set_inactive_style(self):
        self.modify_button.button_style = ''
        self.modify_button.description = 'Modify'
        self.delete_button.disabled = True
        self.delete_button.description = ' '
        self.delete_button.button_style = ''