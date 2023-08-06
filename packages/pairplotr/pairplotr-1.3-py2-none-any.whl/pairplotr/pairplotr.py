import inspect

from textwrap import wrap

import matplotlib

import matplotlib.pyplot as plt
import numpy as np

import matplotlib.colors as colors
import matplotlib.pyplot as mpl_plt
import matplotlib.colors as mpl_colors
import matplotlib.cm as cmx

import time

import pandas as pd

class Inspector(object):
    """
    Class that handles visualizing pandas dataframe data
    """
    def __init__(self, df, categorical_int_limit=10,
                 categorical_order='frequency'):
        # Copy of dataframe
        self.df = df.copy()

        # Order of categorical feature values
        self.categorical_order = categorical_order

        self.feature_value_counts = None

        self.feature_types = None

        self.feature_numerical_flags = None

        self.feature_colors = {}

        # Number of top feature values to display to cut down on processing
        # time
        self.top = None

        # Obtain sorted value count dataframes for each feature
        self._count_feature_values()

        self._set_feature_types(categorical_int_limit=categorical_int_limit)

        self._set_feature_numerical_flags()

    def _set_feature_numerical_flags(self):
        """
        Sets flags indicating whether each feature is or is not numerical
        """
        feature_types = self.feature_types

        numerical_flags = {}
        for feature, feature_type in self.feature_types.iteritems():
            if feature not in numerical_flags:
                feature_is_numerical = ('categorical' not in feature_type \
                                     and feature_type != 'id')

                numerical_flags[feature] = feature_is_numerical
            else:
                raise Exception("Feature %s is duplicated"%(feature))

        self.feature_numerical_flags = numerical_flags

    def _set_feature_types(self, categorical_int_limit=10):
        """
        Automatically determines suspected types of features in dataframe

        Parameters
        ----------
        categorical_int_limit : int, optional
            How many unique values an integer feature needs before it is
            treated as a categorical for the purpose of visualization

        """
        # TODO: Feed categorical_int_limit to the class initialization
        # TODO: Add option to manually set types, either through the dataframe
        # type or through a keyword argument
        # TODO: Check input types

        df = self.df

        feature_value_counts = self.feature_value_counts

        non_null_df = df

        row_count = len(non_null_df)

        feature_types = {}
        for feature in non_null_df.columns:
            unique_value_count = len(feature_value_counts[feature])

            if non_null_df[feature].dtype == int:
                feature_type = 'int'
            elif non_null_df[feature].dtype == float:
                feature_type = 'float'
            else:
                feature_type = 'categorical'

            if row_count == unique_value_count:
                if feature_type in ['int', 'categorical']:
                    feature_type = 'id'

            if (feature_type is 'int'
                and feature_type is not 'id'
                and unique_value_count > 0
                and unique_value_count <= categorical_int_limit):

                feature_type = 'categorical_int'

            if feature not in feature_types:
                feature_types[feature] = feature_type
            else:
                raise Exception(
                    "Feature, %s, is duplicated in dataframe."%(feature))

        self.feature_types = feature_types

    def _count_feature_values(self):
        categorical_order = self.categorical_order

        df = self.df

        feature_value_counts = {}

        for feature in self.df.columns:
            if feature not in feature_value_counts:
                feature_value_counts[feature] = {}

            # Set order
            if categorical_order == 'descending':
                sorted_df = \
                    df[feature].value_counts(dropna=False).sort_index(
                        ascending=False)
            elif categorical_order == 'ascending':
                sorted_df = \
                    df[feature].value_counts(dropna=False).sort_index(
                        ascending=True)
            elif categorical_order == 'frequency':
                sorted_df = \
                    df[feature].value_counts(dropna=False).sort_values(
                        ascending=False)
            else:
                raise Exception("'categorical_order' keyword argument %s" \
                                " not recognized."%(categorical_order))

            feature_value_counts[feature] = sorted_df

        self.feature_value_counts = feature_value_counts

    def _set_feature_value_colors(self, plot_vars, top='all',
                                  color_map='viridis'):
        """
        Chooses colors for feature values with the top counts
        """
        # Set matplotlib based on wehther custom colors are specified or not
        if isinstance(color_map, str):
            if color_map == 'custom':
                # Set custom colors
                custom_map = ['gray', 'cyan', 'orange', 'magenta', 'lime',
                                 'red', 'purple', 'blue', 'yellow', 'black']

                mpl_cmap = None
            else:
                # Get matplotlib color map
                mpl_cmap = mpl_plt.get_cmap(color_map)

        elif isinstance(color_map, list):
            mpl_cmap = None

            custom_map = color_map

        numerical_flags = self.feature_numerical_flags

        feature_value_counts = self.feature_value_counts

        feature_value_colors = {}

        for feature in plot_vars:
            feature_specific_value_counts = feature_value_counts[feature]

            if feature not in feature_value_colors:
                feature_value_colors[feature] = {}

            feature_is_numerical = numerical_flags[feature]

            if not feature_is_numerical:
                # Obtain the value count dataframe for this feature and trim
                # to top number of desired values
                if top == 'all':
                    trimmed_value_counts = feature_specific_value_counts
                else:
                    trimmed_value_counts = \
                        feature_specific_value_counts.iloc[:top]

                    # trimmed_value_counts = \
                    #     feature_specific_value_counts.nlargest(top)

                sorted_values = trimmed_value_counts.index

                feature_value_count = len(sorted_values)

                if mpl_cmap is not None:
                    scalar_map = cmx.ScalarMappable(
                        norm=mpl_colors.Normalize(
                            vmin=0,
                            vmax=feature_value_count-1
                        ),
                        cmap=mpl_cmap
                    )
                else:
                    scalar_map = custom_map[:feature_value_count]

                for color_ind, feature_value in enumerate(sorted_values):
                    if mpl_cmap is not None:
                        color = scalar_map.to_rgba(color_ind)
                    else:
                        color = scalar_map[color_ind]

                    feature_value_colors[feature][feature_value] = color

        self.feature_colors = feature_value_colors

    def _get_default_kwargs(self, kwarg_type, row_count=None, col_count=None):
        """
        Returns kwarg dictionary given the desired type.

        Parameters
        ----------
        kwarg_type :    str, {'subplot'}
            Type of default keyword arguments to return.
            subplot :   Default keyword arguments for individual subplots of a
                        multi-subplot figure
        """
        default_subplot_kwargs = dict(
            title = '',
            facecolor = 'white', # fc overrides this so it's not set
            alpha =	1.0, # float (0.0 transparent through 1.0 opaque)
            frame_on = True, # [ True | False ]
            visible = True, # [True | False]
            xlabel = '',
            xlim = None, #Use with autoscalex_on set to False to constrain subplots
            autoscalex_on = True, # Set to False and specify xlim to constrain subplots
            xmargin = 0.05, # Percent of range of x data to use to pad around x-axis (Ex: 0-40 range w/ xmargin=0.5 pads an extra 20 on both left and right. Seems default is 0.05)
            xscale = 'linear', # ['linear' | 'log' | 'logit' | 'symlog']
            # xticklabels = [], # Can set this externally if desired
            # xticks = [], # Can set this externally if desired
            ylabel = '',
            # ylim = None, # Must be set externally, unlike xlim and autoscalex_on, for similar behavior
            autoscaley_on = True,
            ymargin = 0.05, # Percent of range of y data to use to pad above the y-axis (Ex: 0-40 range w/ xmargin=0.5 pads an extra 20 on above. Seems default is 0.05)
            yscale = 'linear', # ['linear' | 'log' | 'logit' | 'symlog']
            # yticklabels = [], # Can set this externally if desired
            # yticks = [], # Can set this externally if desired
            zorder = None, # Order relative to other elements
        )

        if kwarg_type == 'subplot':
            default_kwargs = default_subplot_kwargs
        elif kwarg_type == 'fig':
            # Check the number of rows and columns
            if type(row_count) is not int \
                or (type(row_count) is int and row_count < 1):

                raise Exception("The keyword argument determining the number " \
                                "of rows in the multi-subplot figure, " \
                                "row_count, must be set as a number larger " \
                                "than or equal to 1.")

            if type(row_count) is not int\
                or (type(row_count) is int and row_count < 1):

                raise Exception("The keyword argument determining the number " \
                                "of columns in the multi-subplot figure, " \
                                "col_count, must be set as a number larger " \
                                "than or equal to 1.")


            default_fig_kwargs = dict(
                # Figure kwargs
                nrows=row_count,
                ncols=col_count,
                sharex=False,
                sharey=False,
                squeeze=False,
                gridspec_kw=None,
                # Figure kwargs
                figsize=(10, 8*row_count), #(10, 300)
                facecolor='white',
                # Subplots kwargs
                subplot_kw = default_subplot_kwargs,
            )

            default_kwargs = default_fig_kwargs
        else:
            raise Exception("Kwarg type, %s, is not recognized." % (kwarg_type))

        return default_kwargs

    def _set_visible_spines(self, ax, visible_spines,
                            text_and_line_color='black',
                            line_width=1.0):
        spine_ids = ['top', 'bottom', 'left', 'right']

        # Set visible frame attributes
        for spine_id in visible_spines:
            ax.spines[spine_id].set_linewidth(line_width)
            ax.spines[spine_id].set_color(text_and_line_color)

        invisible_spine_ids = [spine_id for spine_id in spine_ids \
                               if spine_id not in visible_spines]

        # Remove spines
        for spine_id in invisible_spine_ids:
            ax.spines[spine_id].set_visible(False)

    def _set_grid_lines(self, ax, line_axis, grid_kwargs=None):
        """
        Used to set only major grid lines of a particular axis as on.

        Parameters
        ----------
        ax :    matplotlib.axes._subplots.AxesSubplot
            Axis to apply the settings to
        line_axis : str, {'x', 'y'}
            Axis to set to visible (other is set to invisible)
            'x' :   Major grid lines of x-axis are visible
            'y' :   Major grid lines of y-axis are visible
        grid_kwargs :   dict, optional
            Keyword arguments that can be applied to
            matplotlib.axes._subplots.AxesSubplot.yaxis.grid method (or
            xaxis.grid version) to set the line properties.
            See https://matplotlib.org/api/lines_api.html for options.
        """

        default_grid_kwargs = dict(
            linestyle='--',
            linewidth=1,
            alpha=1.0,
            antialiased=False,
            color='grey',
            zorder=1
        )

        # Override defaults if user provides kwargs
        if grid_kwargs is not None:
            for key, item in grid_kwargs.iteritems():
                default_grid_kwargs[key] = item

        if line_axis == 'y':
            ax.yaxis.grid(True, **default_grid_kwargs)
        elif line_axis == 'x':
            ax.xaxis.grid(True, **default_grid_kwargs)

    def _draw_feature_distribution(self, ax, feature,
                                   hist_kwargs=None, top='all',
                                   grid_kwargs=None,
                                   text_and_line_color='black',
                                   line_width=1.0, max_bar_label_width=20):
        """
        """
        default_color = 'grey'

        df = self.df

        feature_colors = self.feature_colors

        feature_is_numerical = self.feature_numerical_flags[feature]

        value_counts = self.feature_value_counts[feature]

        if top == 'all':
            trimmed_value_counts = value_counts
        else:
            trimmed_value_counts = value_counts.iloc[:top]

        if feature_is_numerical:
            feature_values = df[feature].values

            non_null_mask = ~np.isnan(feature_values)

            if non_null_mask.any():
                non_null_values = feature_values[non_null_mask]

                self._draw_hist(ax, non_null_values, hist_kwargs=hist_kwargs)

                # Draw only bottom spine
                visible_spines = ['bottom']
                self._set_visible_spines(ax, visible_spines,
                                         text_and_line_color=text_and_line_color,
                                         line_width=line_width)

                self._set_grid_lines(ax, 'y', grid_kwargs=grid_kwargs)
        else:
            original_labels = trimmed_value_counts.index.values

            bar_values = trimmed_value_counts.values

            tick_labels = []
            for original_label_ind in xrange(len(original_labels)):
                original_label = original_labels[original_label_ind]

                # Convert null labels to 'NaN'
                if pd.isnull(original_label):
                    new_label = 'NaN'
                else:
                    new_label = original_label


                if type(new_label) is str:
                    if len(new_label)>max_bar_label_width:
                        new_label = new_label[:max_bar_label_width-3]+'...'
                    else:
                        new_label = new_label
                else:
                    new_label = new_label

                tick_labels.append(new_label)

            plot_colors = []
            for feature_value in tick_labels:
                if feature in feature_colors:
                    feature_value_color_set = feature_colors[feature]

                    if feature_value in feature_value_color_set:
                        color = feature_value_color_set[feature_value]

                        plot_colors.append(color)
                    else:
                        plot_colors.append(default_color)

                        print "WARNING: Value, ", feature_value, ", "\
                              "corresponding to feature %s was not found" \
                              % (feature)
                else:
                    plot_colors = default_color

            if top != 'all':
                plot_colors = plot_colors[:top]

            self._draw_bar(ax, tick_labels, bar_values, bar_colors=plot_colors)

            # Draw only bottom spine
            visible_spines = ['left']
            self._set_visible_spines(ax, visible_spines,
                                     text_and_line_color=text_and_line_color,
                                     line_width=line_width)

            self._set_grid_lines(ax, 'x', grid_kwargs=grid_kwargs)

    def _draw_bar(self, ax, tick_labels, bar_values, bar_colors=None):
        # Derive bar positions
        bar_positions = np.arange(len(bar_values))

        # Reshape if given flat arrays
        if len(bar_values.shape) == 1:
            bar_values = bar_values.reshape(-1, 1)

            bar_colors = [bar_colors]

        # Set bar positions as starting from the top of the axis (bottom
        # is default)
        bar_positions = np.arange(bar_values.shape[0])[::-1]

        # Initialize bottom bar buffer
        bottom_bar_buffer = np.zeros(bar_values.shape[0])

        # Plot stacked bars for row feature data corresponding to each column feature value
        for data_ind in xrange(bar_values.shape[1]):
            data = bar_values[:,data_ind]

            # Add previous values to current buffer
            if data_ind:
                bottom_bar_buffer = bottom_bar_buffer + bar_values[:, data_ind-1]

            current_colors = bar_colors[data_ind]

            # Set series-specific parameters
            # Set lower value to start bars from
            bar_kwargs = dict(
                height=0.8,
                left=bottom_bar_buffer,
                color=current_colors,
                tick_label=tick_labels,
                zorder=1000,
                edgecolor=current_colors
            )

            ax.barh(bar_positions, data, **bar_kwargs)

    def _draw_hist(self, ax, x, colors='grey', hist_kwargs=None):
        """
        Draws histogram of on provided axis using the provided data
        """
        if type(colors) is not list:
            colors = [colors]

        if type(x) is not list:
            x = [x]

        # Make base hist kwargs
        patch_color = 'grey'
        default_hist_kwargs = dict(
            bins=20,
            range=None,
            normed=False,
            weights=None,
            cumulative=False,
            bottom=None,
            histtype='bar',
            align='mid',
            orientation='vertical',
            rwidth=None,
            log=False,
            label=None,
            stacked=False,
            zorder=1000,
            # Patch kwargs
            color=patch_color,
            edgecolor='white',
            #facecolor=None, # Have to comment this out so that it defaults
                             # to color kwarg
            linewidth=1.0,
            linestyle='-',
            antialiased=None,
            hatch=None,
            fill=True,
            # capstyle='projecting', No clue what this is and the default gives error
            # joinstyle=None
        )

        # Override defaults for histogram parameters if provided by user
        if hist_kwargs is not None:
            for key, value in hist_kwargs.iteritems():
                default_hist_kwargs[key] = value

        # Find max and min values in all data
        data_mins = []
        data_maxs = []
        for data in x:
            non_null_mask = ~np.isnan(data)
            if non_null_mask.any():
                data_min = data.min()
                data_max = data.max()

                data_mins.append(data_min)
                data_maxs.append(data_max)

        if data_mins and data_maxs:
            if 'range' in default_hist_kwargs:
                if default_hist_kwargs['range'] is None:
                    all_data_min = np.min(data_mins)
                    all_data_max = np.max(data_maxs)
                else:
                    all_data_min = default_hist_kwargs['range'][0]
                    all_data_max = default_hist_kwargs['range'][1]
            else:
                all_data_min = np.min(data_mins)
                all_data_max = np.max(data_maxs)

            # Set bin bounds for cleaner plots
            if not default_hist_kwargs['stacked']:
                if all_data_min != all_data_max:
                    default_hist_kwargs['bins'] = \
                        np.linspace(all_data_min, all_data_max,
                                    default_hist_kwargs['bins'])
                else:
                    default_hist_kwargs['bins'] = None

                for data_series_ind, data_series in enumerate(x):
                    color = colors[data_series_ind]

                    default_hist_kwargs['color'] = color
                    default_hist_kwargs['facecolor'] = color

                    ax.hist(data_series, **default_hist_kwargs)
            else:
                default_hist_kwargs['range'] = [all_data_min, all_data_max]

                default_hist_kwargs['color'] = colors

                ax.hist(x, **default_hist_kwargs)

            # Collect Patch objects representing bars at the same position
            bars = {}
            for bar in ax.patches:
                # Get current bar position
                bar_position = bar.get_x()

                # Initialize x-position list in bar dictionary if not present
                if bar_position not in bars:
                    bars[bar_position] = []

                # Add current bar to collection of bars at that position
                bars[bar_position].append(bar)

            # Sort bars based on height so smallest is visible
            for bar_position, bar_group in bars.iteritems():
                # Sort bars by height order for current bar group at current position
                if len(bar_group) > 1:
                    # Sort by height
                    bar_group = sorted(bar_group,
                                       key=lambda x: x.get_height(), reverse=True)

                    # Set layer position to current order
                    for bar_ind,bar in enumerate(bar_group):
                        bar.set_zorder(bar_ind+2)

    # def fast_plot(self, target_feature):
    #     # target_feature = 'rootznaws'
    #
    #     plot_vars = sorted([column for column in self.df.columns if column != target_feature])
    #
    #     for feature_ind, feature in enumerate(plot_vars):
    #         if not feature_ind:
    #             show_target = True
    #         else:
    #             show_target = False
    #
    #         self.Inspector(e1_df[[feature, target_feature]]).inspect_data(
    #             top=10, target_feature=target_feature,
    #             fig_kwargs={'figsize': (10, 10)}, show_target=show_target
    #         )
    #
    #         plt.show()

    def inspect_data(self, plot_vars=None, target_feature=None,
                     subplot_kwargs=None, fig_kwargs=None, feature_limit=15,
                     hist_kwargs=None, grid_kwargs=None, scatter_kwargs=None,
                     color_map='viridis', show_target=None,
                     plot_whole_figure=False, max_bar_label_width=20,
                     show_all_null=False, custom_hist_range=None,
                     custom_bins=None, bins=20):
        """
        Plots data distributions (histogram for numerical and horizontal bar
        chart for non-numerical) for each feature alongside the response of
        target feature (if specified)
        """
        plt.close('all')

        if show_all_null:
            df = self.df
        else:
            df = self.df.dropna(axis=1, how='all')

        if plot_vars is None:
            plot_vars = sorted([column for column in df.columns \
                                if column != target_feature])

        if not plot_whole_figure:
            for feature_ind, feature in enumerate(plot_vars):
                if show_target is None:
                    if not feature_ind:
                        tmp_show_target = True
                    else:
                        tmp_show_target = False
                else:
                    tmp_show_target = show_target

                if target_feature:
                    tmp_plot_vars = [feature, target_feature]
                else:
                    tmp_plot_vars = [feature]

                # Modify range of histogram
                if type(custom_hist_range) is dict:
                    if feature in custom_hist_range:
                        feature_range = custom_hist_range[feature]
                    else:
                        feature_range = None
                else:
                    feature_range=custom_hist_range

                # Modify number of bins based on feature
                if type(custom_bins) is dict:
                    if feature in custom_bins:
                        feature_bins = custom_bins[feature]
                    else:
                        feature_bins = bins
                else:
                    feature_bins = bins

                if type(hist_kwargs) is dict:
                    hist_kwargs['range'] = feature_range
                    hist_kwargs['bins'] = feature_bins
                else:
                    hist_kwargs = dict(
                        range = feature_range,
                        bins = feature_bins
                    )

                self.inspect_all_data(plot_vars=tmp_plot_vars,
                                      target_feature=target_feature,
                                      subplot_kwargs=subplot_kwargs,
                                      fig_kwargs=fig_kwargs,
                                      top=feature_limit,
                                      hist_kwargs=hist_kwargs,
                                      grid_kwargs=grid_kwargs,
                                      scatter_kwargs=scatter_kwargs,
                                      color_map=color_map,
                                      show_target=tmp_show_target,
                                      max_bar_label_width=max_bar_label_width)
                plt.show()
        else:
            self.inspect_all_data(target_feature=target_feature,
                                  subplot_kwargs=subplot_kwargs,
                                  fig_kwargs=fig_kwargs,
                                  top=feature_limit,
                                  hist_kwargs=hist_kwargs,
                                  grid_kwargs=grid_kwargs,
                                  scatter_kwargs=scatter_kwargs,
                                  color_map=color_map,
                                  show_target=show_target,
                                  max_bar_label_width=max_bar_label_width)

    def inspect_all_data(self, plot_vars=None, target_feature=None,
                     subplot_kwargs=None, fig_kwargs=None, top='all',
                     hist_kwargs=None, grid_kwargs=None, scatter_kwargs=None,
                     color_map='viridis', show_target=True, plot_fast=False,
                     max_bar_label_width=20):
        """
        Plots data distributions (histogram for numerical and horizontal bar
        chart for non-numerical) for each feature alongside the response of
        target feature (if specified)
        """
        df = self.df

        feature_types = self.feature_types

        numerical_flags = self.feature_numerical_flags

        # Initialize plotted features to all if not provided
        if plot_vars is None:
            features = sorted(feature_types.keys())
            if target_feature:
                plot_vars = [key for key in features
                             if key != target_feature]

                if show_target:
                    plot_vars.insert(0, target_feature)
            else:
                plot_vars = features
        else:
            if target_feature:
                if target_feature in plot_vars:
                    target_feature_ind = plot_vars.index(target_feature)

                    _ = plot_vars.pop(target_feature_ind)

                    if show_target:
                        plot_vars.insert(0, target_feature)

        # Get relevant feature value colors
        if target_feature:
            target_is_numerical = numerical_flags[target_feature]

            if not target_is_numerical:
                self._set_feature_value_colors(
                    [target_feature], top=top, color_map=color_map)
            else:
                self._set_feature_value_colors(
                    plot_vars, top=top, color_map=color_map)

        # Calulate plot dimensions
        row_count = len(plot_vars)
        if target_feature is not None:
            col_count = 2
        else:
            col_count = 1

        # Set general settings for individual subplots
        default_subplot_kwargs = self._get_default_kwargs('subplot')

        # Override default subplot kwargs if provided by user
        if subplot_kwargs is not None:
            for key, value in subplot_kwargs.iteritems():
                default_subplot_kwargs[key] = value

        # Set default figure parameters
        default_fig_kwargs = self._get_default_kwargs('fig',
                                                      row_count=row_count,
                                                      col_count=col_count)

        # Override default figure kwargs if provided by user
        if fig_kwargs is not None:
            for key, value in fig_kwargs.iteritems():
                default_fig_kwargs[key] = value

        if not show_target:
            default_fig_kwargs['figsize']=(default_fig_kwargs['figsize'][0],
                                           default_fig_kwargs['figsize'][1]/2.0)

        # Set default text parameters
        text_font_size = 12
        tick_label_size = text_font_size-3

        text_properties = {
            'tick_labels': {
                'family': 'sans-serif',
                'weight': 'normal',
                'size': tick_label_size,

            }
        }

        small_text_size = 10

        # Set text and line color
        grayLevel = 0.6
        text_and_line_color = (0.0, 0.0, 0.0, grayLevel)

        # Set line properties
        line_width = 1.0

        # Set padding of axis labels so they don't overlap with tick-labels
        label_padding = 0.05

        # Initialize plot (Kwarg 'squeeze' used to make output a matrix, even if
        # there is only one plot. This makes indexing more consistent.)
        fig, sub_axes = plt.subplots(**default_fig_kwargs)

        # Get counts of all features
        df_counts = df.count()

        df_row_count = len(df)

        # Fill figure cells
        for row_ind in xrange(row_count):
            feature = plot_vars[row_ind]

            feature_type = feature_types[feature]

            feature_is_numerical = self.feature_numerical_flags[feature]

            non_null_count = df_counts[feature]

            # Derive feature distribution plot title
            title = '%s:    (%d/%d)' % (feature, non_null_count, df_row_count)

            for col_ind in xrange(col_count):

                # Obtain current axis
                ax = sub_axes[row_ind, col_ind]

                # Fill row with feature distribution if on left edge and response
                # of target feature if on right edge
                if not col_ind:
                    # Graph feature distrubution
                    self._draw_feature_distribution(
                        ax, feature, top=top, hist_kwargs=hist_kwargs,
                        grid_kwargs=grid_kwargs, line_width=line_width,
                        text_and_line_color=text_and_line_color,
                        max_bar_label_width=max_bar_label_width
                    )

                    ax.set_title(title, color=text_and_line_color,
                                 size=text_font_size)
                else:
                    if row_ind:
                        self._draw_target_vs_feature(
                            ax, feature, target_feature, top=top,
                            text_and_line_color=text_and_line_color,
                            line_width = line_width, grid_kwargs=grid_kwargs,
                            hist_kwargs=hist_kwargs,
                            scatter_kwargs=scatter_kwargs
                        )
                    else:
                        if show_target:
                            ax.axis('off')
                        else:
                            self._draw_target_vs_feature(
                                ax, feature, target_feature, top=top,
                                text_and_line_color=text_and_line_color,
                                line_width = line_width, grid_kwargs=grid_kwargs,
                                hist_kwargs=hist_kwargs,
                                scatter_kwargs=scatter_kwargs
                            )


                # Remove ticks
                ax.tick_params(axis=u'both', which=u'both',length=0)

                # Set x-tick label sizes and colors
                for x_tick in ax.xaxis.get_major_ticks():
                    x_tick.label.set_fontsize(small_text_size)
                    x_tick.label.set_color(text_and_line_color)

                # Set x-tick label sizes and colors
                for y_tick in ax.yaxis.get_major_ticks():
                    y_tick.label.set_fontsize(small_text_size)
                    y_tick.label.set_color(text_and_line_color)

                # Remove ticks but not labels
                ax.tick_params(axis=u'both', which=u'both',length=0)

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
                            wspace=None, hspace=0.35)

        # plt.close(fig)

    def _draw_numerical_vs_numerical(self, ax, feature, target_feature,
                                     scatter_kwargs=None):
        """
        Draws scatter plot of target_feature versus feature
        """
        default_scatter_kwargs = dict(
            s = 100.0,    # scalar or array_like, shape (n, ), optional
            c = 'grey', # color, sequence, or sequence of color, optional,
                        # default: 'b'
            marker = 'o',   # MarkerStyle, optional, default: 'o'
            cmap = None,    # Colormap, optional, default: None
            norm = None,    # Normalize, optional, default: None. A Normalize
                            # instance is used to scale luminance data to 0, 1.
                            # norm is only used if c is an array of floats.
                            # If None, use the default normalize().

            alpha = 0.6,   # scalar, optional, default: None. The alpha
                            # blending value, between 0 (transparent) and
                            # 1 (opaque)
            linewidths = 1.0,  # scalar or array_like, optional, default: None
                                # If None, defaults to (lines.linewidth,).
            edgecolors = 'white',  # color or sequence of color, optional,
                                # default: None. If None, defaults to 'face'.
                                # If 'face', the edge color will always be the
                                # same as the face color. If it is 'none',
                                # the patch boundary will not be drawn. For
                                # non-filled markers, the edgecolors kwarg is
                                # ignored and forced to 'face' internally.
        )

        if scatter_kwargs is not None:
            for key, item in scatter_kwargs.iteritems():
                default_scatter_kwargs[key] = item

        df = self.df

        df.plot(kind='scatter', ax=ax, x=feature, y=target_feature,
                **default_scatter_kwargs)

    def _draw_target_vs_feature(self, ax, feature, target_feature, top='all',
                                text_and_line_color='black', line_width=1.0,
                                grid_kwargs=None, hist_kwargs=None,
                                scatter_kwargs=None):
        """
        """
        feature_numerical_flags = self.feature_numerical_flags

        feature_is_numerical = feature_numerical_flags[feature]
        target_is_numerical = feature_numerical_flags[target_feature]

        if target_is_numerical:
            if feature_is_numerical:
                # Draw uncolored scatter plot
                self._draw_numerical_vs_numerical(ax, feature, target_feature,
                                                  scatter_kwargs=scatter_kwargs)

                # Draw only bottom spine
                visible_spines = ['bottom']
                self._set_visible_spines(ax, visible_spines,
                                         text_and_line_color=text_and_line_color,
                                         line_width=line_width)

                self._set_grid_lines(ax, 'y', grid_kwargs=grid_kwargs)

                ax.xaxis.label.set_visible(False)
                ax.yaxis.label.set_visible(False)
            else:
                # Draw target histograms colored by feature category values
                self._draw_categorical_vs_numerical(ax, target_feature, feature,
                                                    top=top,
                                                    hist_kwargs=hist_kwargs)
                # Draw only bottom spine
                visible_spines = ['bottom']
                self._set_visible_spines(ax, visible_spines,
                                         text_and_line_color=text_and_line_color,
                                         line_width=line_width)

                self._set_grid_lines(ax, 'y', grid_kwargs=grid_kwargs)

        else:
            if feature_is_numerical:
                # Draw feature histograms colored by target category values
                hue_feature = target_feature

                self._draw_categorical_vs_numerical(ax, feature, hue_feature,
                                                    top=top,
                                                    hist_kwargs=hist_kwargs)
                # Draw only bottom spine
                visible_spines = ['bottom']
                self._set_visible_spines(ax, visible_spines,
                                         text_and_line_color=text_and_line_color,
                                         line_width=line_width)

                self._set_grid_lines(ax, 'y', grid_kwargs=grid_kwargs)
            else:
                # Draw stacked horizontal bar chart of feature distribution
                # colored by target category values
                hue_feature = target_feature

                self._draw_categorical_vs_categorical(ax, feature, hue_feature,
                                                      top=top)

                # Draw only bottom spine
                visible_spines = ['left']
                self._set_visible_spines(ax, visible_spines,
                                         text_and_line_color=text_and_line_color,
                                         line_width=line_width)

                self._set_grid_lines(ax, 'x', grid_kwargs=grid_kwargs)


    def _draw_categorical_vs_numerical(self, ax, feature, hue_feature,
                                       top='all', hist_kwargs=None):
        """
        Draws, on the provided axis artist, histograms of the feature colored
        by each value of the hue feature.
        """
        df = self.df

        hue_value_colors = self.feature_colors[hue_feature]

        value_counts = self.feature_value_counts

        ordered_hue_values = value_counts[hue_feature].index.values

        if top == 'all':
            trimmed_ordered_hue_values = ordered_hue_values
        else:
            trimmed_ordered_hue_values = ordered_hue_values[:top]

        colors = []
        data = []
        for hue_value in trimmed_ordered_hue_values:
            color = hue_value_colors[hue_value]

            colors.append(color)

            feature_values_for_hue_value_df = \
                df[feature][df[hue_feature]==hue_value]

            non_null_values = \
                feature_values_for_hue_value_df[
                    feature_values_for_hue_value_df.notnull()].values

            data.append(non_null_values)

            # data.append(feature_values_for_hue_value)

        self._draw_hist(ax, data, colors=colors, hist_kwargs=hist_kwargs)

    def _draw_categorical_vs_categorical(self, ax, feature, hue_feature,
                                         top='all'):
        """
        Draws stacked horizontal bar chart of categorical feature data colored
        by the values of the hue feature.
        """
        df = self.df

        hue_value_colors = self.feature_colors[hue_feature]

        value_counts = self.feature_value_counts[feature]

        if top == 'all':
            trimmed_value_counts = value_counts
        else:
            trimmed_value_counts = value_counts.iloc[:top]

        feature_values = trimmed_value_counts.index.values

        hue_feature_values = self.feature_value_counts[hue_feature].index.values

        counts = np.zeros([len(hue_feature_values), len(feature_values)])
        colors = np.zeros([len(hue_feature_values), len(feature_values)],
                          dtype=object)

        for feature_value_ind, feature_value in enumerate(feature_values):
            if feature_value is np.nan:
                where = df[feature] == feature_value
            else:
                where = df[feature].isnull()



            hue_data_for_feature_value = \
                df[hue_feature][where]

            hue_counts_for_feature_value = \
                hue_data_for_feature_value\
                    .value_counts(dropna=False).sort_values(ascending=False)

            if feature_value is not np.nan:
                hue_counts_for_feature_value = df[hue_feature][df[feature]==feature_value].value_counts(dropna=False).sort_values(ascending=False)
            else:
                hue_counts_for_feature_value = df[hue_feature][df[feature].isnull()].value_counts(dropna=False).sort_values(ascending=False)

            found_hue_features = hue_counts_for_feature_value.index.values

            missing_hue_values = set(hue_feature_values)-set(found_hue_features)

            for missing_hue_value in missing_hue_values:
                hue_counts_for_feature_value.loc[missing_hue_value] = 0

            hue_values = hue_counts_for_feature_value.index.values
            hue_counts = hue_counts_for_feature_value.values

            for hue_value_ind, hue_value in enumerate(hue_values):
                hue_count = hue_counts[hue_value_ind]

                counts[hue_value_ind, feature_value_ind] = hue_count

                color = hue_value_colors[hue_value]

                colors[hue_value_ind, feature_value_ind] = color

        tick_labels = ''
        bar_values = counts
        bar_colors = colors

        self._draw_bar(ax, tick_labels, bar_values.T, bar_colors=bar_colors)



        # self._draw_bar(ax, tick_labels, bar_values.T, color=colors, title='',
        #          text_font_size=text_font_size,
        #          text_and_line_color=text_and_line_color,
        #          small_text_size=small_text_size)

            # for hue_value in hue_counts_for_feature_value.index.values:
            #     hue_count = hue_counts_for_feature_value.loc[hue_value]
            #
            #     print hue_value, hue_count

            # for target_value_count_ind, target_value_count in enumerate()
            # for target_value_count_ind, target_value_count in enumerate(target_value_counts):
            #     counts[target_value_count_ind, feature_value_ind] = target_value_count
            #
            #     target_value = target_values[target_value_count_ind]
            #
            #     color = feature_value_colors[target_feature][target_value]
            #
            #     colors[target_value_count_ind, feature_value_ind] = color







        #
        # for hue_feature_value in hue_feature_values:
        #     target_value_mask = df[hue_feature]==hue_feature_value
        #
        #     current_feature_values = df[feature][target_value_mask]
        #
        #     if top == 'all':
        #         trimmed_feature_values_df = \
        #             current_feature_values\
        #                 .value_counts(dropna=False).sort_values(ascending=True)
        #     else:
        #         trimmed_feature_values_df = \
        #             current_feature_values\
        #                 .value_counts(dropna=False)\
        #                 .sort_values(ascending=True).nlargest(top)
        #
        #     print '\t', hue_feature_value
        #     print '\t', trimmed_feature_values_df





# def draw_target_vs_feature(ax, df, feature, target_feature, feature_types,
#                            feature_value_colors, top='all', tick_labels=None,
#                            text_and_line_color='black',
#                            text_font_size=12, small_text_size=9):
#     """
#
#     """
#     # Make copy of dataframe so it's not changed
#     df = df.copy()
#
#     # Fill dataframe with replacements for NaNs for visualization
#     df = df.fillna(value='tmp_nan')
#
#     # # Initialize plotted features to all if not provided
#     # if plot_vars is None:
#     #     if target_feature:
#     #         plot_vars = [key for key in feature_types.keys()
#     #                      if key != target_feature]
#     #
#     #         plot_vars.insert(0, target_feature)
#     #     else:
#     #         plot_vars = feature_types.keys()
#     #
#     # feature_value_colors = \
#     #     ppr.assign_feature_value_colors(df, plot_vars, feature_types, top=top)
#
#
#
#
#     # # Get feature name from series
#     # feature_series = df[feature]
#     #
#     feature_type = feature_types[feature]
#
#     # Set flag indicating whether the feature is numerical or not
#     feature_numerical = \
#         ('categorical' not in feature_type and feature_type != 'id')
#     #
#     # target_series = df[target_feature]
#     #
#     target_feature_type = feature_types[target_feature]
#
#     target_numerical = \
#         ('categorical' not in target_feature_type
#          and target_feature_type != 'id')
#     #
#     # sorted_target_count_df = \
#     #     target_series.value_counts(
#     #         dropna=False).sort_values(ascending=False)
#     #
#     # sorted_target_values = \
#     #     sorted_target_count_df.index.values[::-1]
#     #
#     # # Sort feature values
#     # sorted_value_count_df = \
#     #     feature_series.value_counts(
#     #         dropna=False).sort_values(ascending=False)
#     #
#     # # Replace NaN index w/ string
#     # sorted_value_count_df.index = \
#     #     pd.Series(sorted_value_count_df.index).replace(np.nan, 'nan')
#     #
#     # # Cut data off so only top values shown if desired
#     # if top == 'all':
#     #     sorted_feature_values = \
#     #         sorted_value_count_df.index.values
#     # else:
#     #     sorted_feature_values = \
#     #         sorted_value_count_df.index.values[:top]
#
#     if not target_numerical and not feature_numerical:
#         sorted_feature_value_df = df[feature].value_counts(dropna=False).sort_values(ascending=False)
#
#         feature_value_order = list(sorted_feature_value_df[:top].index.values)
#
#         sorted_target_value_df = df[target_feature].value_counts(dropna=False).sort_values(ascending=False)
#
#         sorted_target_values = list(sorted_target_value_df.index.values)
#
#         sorted_target_value_set = set(sorted_target_values)
#
#         counts = np.zeros([len(sorted_target_values), len(feature_value_order)])
#         colors = np.zeros([len(sorted_target_values), len(feature_value_order)], dtype=object)
#         for feature_value_ind, feature_value in enumerate(feature_value_order):
#             target_dist_in_feature_value_df = df[[feature, target_feature]][df[feature]==feature_value][target_feature].value_counts(dropna=False).sort_values(ascending=False)
#
#             target_dist_in_feature_values = list(target_dist_in_feature_value_df.index.values)
#
#             missing_features = sorted_target_value_set-set(target_dist_in_feature_values)
#
#             for missing_feature in missing_features:
#                 target_dist_in_feature_value_df.loc[missing_feature] = 0
#
#             target_value_counts = target_dist_in_feature_value_df.values
#             target_values = target_dist_in_feature_value_df.index.values
#
#             for target_value_count_ind, target_value_count in enumerate(target_value_counts):
#                 counts[target_value_count_ind, feature_value_ind] = target_value_count
#
#                 target_value = target_values[target_value_count_ind]
#
#                 color = feature_value_colors[target_feature][target_value]
#
#                 colors[target_value_count_ind, feature_value_ind] = color
#
#         # Get pivot table
#         target_dist_in_feature = df[[feature, target_feature]].pivot_table(
#                     columns=[target_feature],
#                     index=[feature],
#                     aggfunc=len).fillna(0,inplace=False)
#
#         # Get the descending order of feature values
#         feature_value_order = list(df[feature].value_counts(dropna=False).sort_values(ascending=False).index.values)
#
#         all_target_values = list(df[target_feature].unique())
#
#         counts = np.zeros(target_dist_in_feature.shape[::-1])
#         colors = np.zeros(target_dist_in_feature.shape[::-1], dtype=object)
#         for feature_value_ind, feature_value in enumerate(feature_value_order):
#             # Get the descending order of target values corresponding to the
#             # current feature value
#             target_value_order = list(df[df[feature] == feature_value][target_feature].value_counts(dropna=False).sort_values(ascending=False).index.values)
#
#             # Add missing target values
#             target_value_order.extend(list(set(all_target_values)-set(target_value_order)))
#
#             # Calculate and save the count of each target feature value and its
#             # corresponding color for the curernt feature value
#             for target_feature_value_ind, target_feature_value in enumerate(target_value_order):
#                 color = feature_value_colors[target_feature][target_feature_value]
#
#                 count = target_dist_in_feature.loc[feature_value][target_feature_value]
#
#                 counts[target_feature_value_ind, feature_value_ind] = count
#
#                 colors[target_feature_value_ind, feature_value_ind] = color
#
#         # if top == 'all':
#         #     sorted_feature_values = \
#         #         sorted_value_count_df.index.values
#         # else:
#         #     sorted_feature_values = \
#         #         sorted_value_count_df.index.values[:top]
#
#
#         if top == 'all':
#             bar_values = counts
#         else:
#             bar_values = counts[:,:top]
#
#
#
#         # plot_bar(ax, tick_labels, bar_values.T, color=colors, title='',
#         #          text_font_size=text_font_size,
#         #          text_and_line_color=text_and_line_color,
#         #          small_text_size=small_text_size)
#
#
#
#
#         # # Pick data and hue features
#         # data_feature = feature
#         # hue_feature = target_feature
#         #
#         # df = df.replace(np.nan, 'nan')
#         #
#         # # Form pivot table between input and output label features
#         # label_by_label = df[[data_feature, hue_feature]].pivot_table(
#         #     columns=[hue_feature],
#         #     index=[data_feature],
#         #     aggfunc=len)
#         #
#         # df = df.replace('nan', np.nan)
#         #
#         # # Order by specific data feature value
#         # label_by_label = label_by_label.loc[reversed(sorted_feature_values)]
#         #
#         # # Fill in N/A values with zero
#         # label_by_label.fillna(0,inplace=True)
#         #
#         # # Obtain column feature
#         # unique_col_feature_values = sorted_target_values
#         #
#         # # Initalize value for bottom bar for stacked bar charts
#         # sorted_row_values = sorted_feature_values
#         #
#         # bottom_bar_buffer = np.zeros(len(sorted_row_values))
#         #
#         # # Set tick-labels
#         # if tick_labels is None:
#         #     tick_labels = sorted_row_values
#         #
#         # # Set bar and tick-label positions
#         # bar_positions = np.arange(len(sorted_row_values))
#         #
#         # unique_col_feature_value_count = len(unique_col_feature_values)
#         #
#         # bar_values = []
#         # colors = []
#         #
#         # bar_values = label_by_label.values
#         #
#         # for unique_col_feature_value_ind, unique_col_feature_value \
#         #     in enumerate(unique_col_feature_values):
#         #
#         #
#         #     color = feature_value_colors[hue_feature][unique_col_feature_value]
#         #     # color = _get_color_val(
#         #     #             unique_col_feature_value_ind,
#         #     #             unique_col_feature_value_count)
#         #
#         #
#         #     colors.append([color for x in xrange(bar_values.shape[0])])
#         #
#         # colors = colors
#
#         # plot_bar(ax, tick_labels, bar_values, color=colors, title='',
#         #          text_font_size=text_font_size,
#         #          text_and_line_color=text_and_line_color,
#         #          small_text_size=small_text_size)
#
#
#     elif target_numerical and not feature_numerical:
#         # Graph numerical target histogram colored by feature
#         pass
#     elif not target_numerical and feature_numerical:
#         # Graph numerical feature histogram colored by target
#         # category
#         pass
#     elif target_numerical and feature_numerical:
#         # Graph scatter plot of target versus feature
#         pass
#     else:
#         raise Exception("Logic error involving choosing subplot " \
#                         "type (e.g. hbar, hist, or scatter) " \
#                         "based on target and feature types " \
#                         "(e.g. numerical or categorical)")
#
#
#     """
#     target = category & feature = category
#         feature stacked hbar chart colored by target
#             Could possibly switch this with a flag
#     target = numerical & feature = category
#         Numerical target histogram colored by feature
#     target = category & feature = numerical
#         Numerical feature histogram colored by target category
#     target = numerical & feature = numerical
#         Scatter plot of target versus feature
#     """

# def inspect_data(plot_vars=None, target_feature=None, subplot_kwargs=None,
#                  fig_kwargs=None, top='all'):
#     """
#     Graphs distribution of each variable and its corresponding effect on the
#     target feature
#     """
#     # Replace NaN temporarily with the string 'nan' for visualization
#     df = df.fillna(value='tmp_nan')
#
#
#     feature_types = _get_feature_types(df)
#
#     # Initialize plotted features to all if not provided
#     if plot_vars is None:
#         if target_feature:
#             plot_vars = [key for key in feature_types.keys()
#                          if key != target_feature]
#
#             plot_vars.insert(0, target_feature)
#         else:
#             plot_vars = feature_types.keys()
#
#     # Get feature value colors
#     feature_value_colors = \
#         assign_feature_value_colors(df, plot_vars, feature_types, top=top)
#
#     # Calulate plot dimensions
#     row_count = len(plot_vars)
#     if target_feature is not None:
#         # row_count = len(plot_vars)-1
#         col_count = 2
#     else:
#         # row_count = len(plot_vars)
#         col_count = 1
#
#     # Set general settings for individual subplots
#     default_subplot_kwargs = dict(
#         title = '',
#         facecolor = 'white', # fc overrides this so it's not set
#         alpha =	1.0, # float (0.0 transparent through 1.0 opaque)
#         frame_on = True, # [ True | False ]
#         visible = True, # [True | False]
#         xlabel = '',
#         xlim = None, #Use with autoscalex_on set to False to constrain subplots
#         autoscalex_on = True, # Set to False and specify xlim to constrain subplots
#         xmargin = 0.05, # Percent of range of x data to use to pad around x-axis (Ex: 0-40 range w/ xmargin=0.5 pads an extra 20 on both left and right. Seems default is 0.05)
#         xscale = 'linear', # ['linear' | 'log' | 'logit' | 'symlog']
#         # xticklabels = [], # Can set this externally if desired
#         # xticks = [], # Can set this externally if desired
#         ylabel = '',
#         # ylim = None, # Must be set externally, unlike xlim and autoscalex_on, for similar behavior
#         autoscaley_on = True,
#         ymargin = 0.05, # Percent of range of y data to use to pad above the y-axis (Ex: 0-40 range w/ xmargin=0.5 pads an extra 20 on above. Seems default is 0.05)
#         yscale = 'linear', # ['linear' | 'log' | 'logit' | 'symlog']
#         # yticklabels = [], # Can set this externally if desired
#         # yticks = [], # Can set this externally if desired
#         zorder = None, # Order relative to other elements
#     )
#
#     # Override default subplot kwargs if provided by user
#     if subplot_kwargs is not None:
#         for key, value in subplot_kwargs.iteritems():
#             default_subplot_kwargs[key] = value
#
#     # Set default figure parameters
#     default_fig_kwargs = dict(
#         # Figure kwargs
#         nrows=row_count,
#         ncols=col_count,
#         sharex=False,
#         sharey=False,
#         squeeze=False,
#         gridspec_kw=None,
#         # Figure kwargs
#         figsize=(5, 100),
#         facecolor='white',
#         # Subplots kwargs
#         subplot_kw = default_subplot_kwargs,
#     )
#
#     # Override default figure kwargs if provided by user
#     if fig_kwargs is not None:
#         for key, value in fig_kwargs.iteritems():
#             default_fig_kwargs[key] = value
#
#     # Set default text parameters
#     text_font_size = 12
#     tick_label_size = text_font_size-3
#
#     text_properties = {
#         'tick_labels': {
#             'family': 'sans-serif',
#             'weight': 'normal',
#             'size': tick_label_size,
#
#         }
#     }
#
#     small_text_size = 10
#
#     # Set text and line color
#     grayLevel = 0.4
#     text_and_line_color = (0.0, 0.0, 0.0, grayLevel)
#
#     # Set grid_kwargs
#     default_grid_kwargs = dict(
#         color = text_and_line_color
#     )
#
#     # Override with provided grid kwargs
#     if grid_kwargs is not None:
#         for key, item in grid_kwargs.iteritems():
#             default_grid_kwargs[key] = item
#
#     # Set padding of axis labels so they don't overlap with tick-labels
#     label_padding = 0.05
#
#     # Initialize plot (Kwarg 'squeeze' used to make output a matrix, even if
#     # there is only one plot. This makes indexing more consistent.)
#     fig, sub_axes = plt.subplots(**default_fig_kwargs)
#
#     # Get counts of all features
#     df_counts = df.count()
#
#     # Fill figure cells
#     for row_ind in xrange(row_count):
#         feature = plot_vars[row_ind]
#
#         feature_type = feature_types[feature]
#
#         feature_series = df[feature]
#
#         non_null_count = df_counts[feature]
#
#         # Derive feature distribution plot title
#         title = '%s:    (%d/%d)' % (feature, non_null_count, len(df))
#
#         for col_ind in xrange(col_count):
#             # Obtain current axis
#             ax = sub_axes[row_ind, col_ind]
#
#             # Fill row with feature distribution if on left edge and response
#             # of target feature if on right edge
#             if not col_ind:
#                 # Graph feature distrubution
#                 draw_feature_distribution(
#                     ax, df, feature, feature_types,
#                     feature_value_colors, text_and_line_color,
#                     top=top, title=title, text_font_size=text_font_size,
#                     small_text_size=small_text_size
#                     )
#
#             else:
#                 if row_ind:
#                     draw_target_vs_feature(
#                         ax, df, feature, target_feature, feature_types,
#                         feature_value_colors=feature_value_colors, top=top,
#                         tick_labels='',
#                         text_and_line_color=text_and_line_color,
#                         text_font_size=text_font_size,
#                         small_text_size=small_text_size)
#                 else:
#                     ax.axis('off')
#
#             ax.tick_params(axis=u'both', which=u'both',length=0)
#
#     plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
#                         wspace=None, hspace=0.35)

    # def _get_color_map(self, color_count):
    #     """
    #     """
    #
    #     if color_map == 'custom':
    #         indexible_map = ['gray', 'cyan', 'orange', 'magenta', 'lime',
    #                          'red', 'purple', 'blue', 'yellow', 'black']
    #     else:
    #         cmap = mpl_plt.get_cmap(color_map)
    #
    #         scalar_map = cmx.ScalarMappable(
    #             norm=mpl_colors.Normalize(vmin=0, vmax=color_count-1),
    #             cmap=cmap)
    #
    #         indexible_map = scalar_map.to_rgba(color_ind)

# def plot_bar(ax, tick_labels, bar_values, color=None, title='',
#              text_and_line_color='black', text_font_size=12,
#              small_text_size=9):
#     """
#     """
#     # # Derive bar positions
#     # bar_positions = np.arange(len(bar_values))
#     #
#     # # Set bar kwargs (bottom (bar positions) and width (widths of bars) are the args)
#     # bar_kwargs = dict(
#     #     height=0.8,
#     #     left=None,
#     #     color=color,
#     #     tick_label=tick_labels,
#     #     zorder=1000,
#     # )
#
#     if len(bar_values.shape) == 1:
#         bar_values = bar_values.reshape(-1, 1)
#
#         color = [color]
#
#     bar_positions = np.arange(bar_values.shape[0])[::-1]
#
#     # Initialize bottom bar buffer
#     bottom_bar_buffer = np.zeros(bar_values.shape[0])
#
#     # Plot stacked bars for row feature data corresponding to each column feature value
#     for data_ind in xrange(bar_values.shape[1]):
#         data = bar_values[:,data_ind]
#
#         # Add previous values to current buffer
#         if data_ind:
#             bottom_bar_buffer = bottom_bar_buffer + bar_values[:, data_ind-1]
#
#         current_colors = color[data_ind]
#
#         # Set series-specific parameters
#         # Set lower value to start bars from
#         bar_kwargs = dict(
#             height=0.8,
#             left=bottom_bar_buffer,
#             color=current_colors,
#             tick_label=tick_labels,
#             zorder=1000,
#             edgecolor=current_colors
#         )
#
#         ax.barh(bar_positions, data, **bar_kwargs)
#
#     # Set left frame attributes
#     ax.spines['left'].set_linewidth(1.0)
#     ax.spines['left'].set_color(text_and_line_color)
#
#     # Remove all but bottom frame line
#     ax.spines['right'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#
#     # Remove ticks but not labels
#     ax.tick_params(axis=u'both', which=u'both',length=0)
#
#     ax.xaxis.grid(True, linestyle='--', linewidth=1)
#
#     ax.set_title(title, color=text_and_line_color, size=text_font_size)
#
#     # Set y-tick label sizes and colors
#     for x_tick in ax.xaxis.get_major_ticks():
#         x_tick.label.set_fontsize(small_text_size)
#         x_tick.label.set_color(text_and_line_color)
#
#     # Set y-tick label sizes and colors
#     for y_tick in ax.yaxis.get_major_ticks():
#         y_tick.label.set_fontsize(small_text_size)
#         y_tick.label.set_color(text_and_line_color)
# def assign_feature_value_colors(df, feature_list, feature_types, top='all'):
#     """
#     """
#     feature_value_colors = {}
#
#     for feature in feature_list:
#         # Get feature type
#         feature_type = feature_types[feature]
#
#         # Initialize new features
#         if feature in feature_value_colors:
#             raise Exception("Feature %s is duplicated"%(feature))
#         else:
#             feature_value_colors[feature] = {}
#
#         feature_is_numerical = ('categorical' not in feature_type \
#                              and feature_type != 'id')
#
#         # Get feature value order, value counts, and color for each value
#         if not feature_is_numerical:
#             # Get feature value counts and sort in ascending order by count
#             if top=='all':
#                 sorted_value_count_df = \
#                     df[feature].value_counts(dropna=False).sort_values(
#                                                                 ascending=True)
#             else:
#                 sorted_value_count_df = \
#                     df[feature].value_counts(dropna=False).sort_values(
#                                                 ascending=True).nlargest(top)
#
#
#             # Get feature values
#             sorted_feature_values = list(sorted_value_count_df.index.values)
#
#             # Get number of feature values
#             feature_value_count = len(sorted_feature_values)
#
#             for feature_value_ind, feature_value in \
#                 enumerate(list(reversed(sorted_feature_values))):
#                 # feature_value_colors[feature][feature_value] = \
#                 #     scalar_map.to_rgba(feature_value_ind)
#
#
#                 feature_value_colors[feature][feature_value] = \
#                     _get_color_val(feature_value_ind, feature_value_count)
#
#
#
#
#     return feature_value_colors


#
# def plot_bar(ax, tick_labels, bar_values, color=None, title='',
#              text_and_line_color='black', text_font_size=12,
#              small_text_size=9):
#     """
#     """
#     # # Derive bar positions
#     # bar_positions = np.arange(len(bar_values))
#     #
#     # # Set bar kwargs (bottom (bar positions) and width (widths of bars) are the args)
#     # bar_kwargs = dict(
#     #     height=0.8,
#     #     left=None,
#     #     color=color,
#     #     tick_label=tick_labels,
#     #     zorder=1000,
#     # )
#
#     if len(bar_values.shape) == 1:
#         bar_values = bar_values.reshape(-1, 1)
#
#         color = [color]
#
#     bar_positions = np.arange(bar_values.shape[0])[::-1]
#
#     # Initialize bottom bar buffer
#     bottom_bar_buffer = np.zeros(bar_values.shape[0])
#
#     # Plot stacked bars for row feature data corresponding to each column feature value
#     for data_ind in xrange(bar_values.shape[1]):
#         data = bar_values[:,data_ind]
#
#         # Add previous values to current buffer
#         if data_ind:
#             bottom_bar_buffer = bottom_bar_buffer + bar_values[:, data_ind-1]
#
#         current_colors = color[data_ind]
#
#         # Set series-specific parameters
#         # Set lower value to start bars from
#         bar_kwargs = dict(
#             height=0.8,
#             left=bottom_bar_buffer,
#             color=current_colors,
#             tick_label=tick_labels,
#             zorder=1000,
#             edgecolor=current_colors
#         )
#
#         ax.barh(bar_positions, data, **bar_kwargs)
#
#     # Set left frame attributes
#     ax.spines['left'].set_linewidth(1.0)
#     ax.spines['left'].set_color(text_and_line_color)
#
#     # Remove all but bottom frame line
#     ax.spines['right'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#
#     # Remove ticks but not labels
#     ax.tick_params(axis=u'both', which=u'both',length=0)
#
#     ax.xaxis.grid(True, linestyle='--', linewidth=1)
#
#     ax.set_title(title, color=text_and_line_color, size=text_font_size)
#
#     # Set y-tick label sizes and colors
#     for x_tick in ax.xaxis.get_major_ticks():
#         x_tick.label.set_fontsize(small_text_size)
#         x_tick.label.set_color(text_and_line_color)
#
#     # Set y-tick label sizes and colors
#     for y_tick in ax.yaxis.get_major_ticks():
#         y_tick.label.set_fontsize(small_text_size)
#         y_tick.label.set_color(text_and_line_color)
#

#
# def draw_feature_distribution(ax, df, feature, feature_types,
#                               feature_value_colors, text_and_line_color,
#                               top='all', title='', text_font_size=12,
#                               small_text_size=10):
#     """
#     """
#     feature_series = df[feature]
#
#     feature_type = feature_types[feature]
#
#     feature_values = feature_series.values
#
#     if ('categorical' not in feature_type
#         and feature_type != 'id'):
#
#         non_null_values = feature_values[~np.isnan(feature_values)]
#
#         if non_null_values.any():
#             plot_hist(ax, non_null_values,
#                       text_and_line_color=text_and_line_color)
#     else:
#         sorted_value_count_df = \
#             feature_series.value_counts(
#                 dropna=False).sort_values(ascending=False)
#
#         if top == 'all':
#             sorted_feature_values = sorted_value_count_df.index.values
#             feature_value_counts = sorted_value_count_df.values
#         else:
#             sorted_feature_values = sorted_value_count_df.index.values[:top]
#             feature_value_counts = sorted_value_count_df.values[:top]
#
#         # Get number of feature values
#         feature_value_count = len(sorted_feature_values)
#
#         color = []
#
#         for feature_value in sorted_feature_values:
#             color.append(feature_value_colors[feature][feature_value])
#
#         color = color
#
#         if top != 'all':
#             color = color[:top]
#
#         plot_bar(ax, sorted_feature_values, feature_value_counts,
#                  color=color, title=title, text_font_size=text_font_size,
#                  small_text_size=small_text_size)
#
#
#
#
#
#
#
#
#
#
# def draw_target_legend(ax, df, target_feature, feature_value_colors,
#                        legend_marker_size=5, legend_font_size=5):
#     """
#     Draws legend
#     """
#     target_feature_series = df[target_feature]
#
#     sorted_target_feature_counts = \
#         target_feature_series.value_counts(dropna=False).sort_values(
#                                                                 ascending=False)
#
#     labels = sorted_target_feature_counts.index.values
#
#     label_count = len(labels)
#
#     target_colors = []
#     for label in labels:
#         color = feature_value_colors[target_feature][label]
#
#         target_colors.append(color)
#
#     # for label_ind in xrange(len(labels)):
#     #
#     #     color = _get_color_val(label_ind, label_count)
#     #
#     #     target_colors.append(color)
#
#     # bar_values = label_by_label.values
#     #
#     # for unique_col_feature_value_ind, unique_col_feature_value \
#     #     in enumerate(unique_col_feature_values):
#     #
#     #     # bar_data = label_by_label[unique_col_feature_value].values
#     #     # bar_values.append(bar_data)
#     #
#     #     color = _get_color_val(
#     #                 unique_col_feature_value_ind,
#     #                 unique_col_feature_value_count)
#     #
#     #
#     #     colors.append([color for x in xrange(bar_values.shape[0])])
#
#     proxies = [create_proxy(color) for color in target_colors]
#
#     custom_legend = (labels, proxies)
#
#     ax.legend(custom_legend[1], custom_legend[0],
#               handlelength=legend_marker_size,
#               handleheight=legend_marker_size,
#               frameon=False, loc='best', fontsize=legend_font_size)
#
#     # plt.setp(plt.gca().get_legend().get_texts(),
#     #          fontsize=legend_font_size)
#
# def create_proxy(color):
#     rect = plt.Rectangle((0,0), 1, 1, color=color)
#
#     return rect
#
#
# def plot_hist(ax, x, hist_kwargs=None, text_and_line_color=None):
#     """
#     """
#
#
#     patch_color = _get_color_val(0,1)
#
#     default_hist_kwargs = dict(
#         bins=20,
#         range=None,
#         normed=False,
#         weights=None,
#         cumulative=False,
#         bottom=None,
#         histtype='bar',
#         align='mid',
#         orientation='vertical',
#         rwidth=None,
#         log=False,
#         label=None,
#         stacked=False,
#         zorder=1000,
#         # Patch kwargs
#         color=patch_color,
#         edgecolor='white',
#         facecolor=patch_color,
#         linewidth=1.0,
#         linestyle='-',
#         antialiased=None,
#         hatch=None,
#         fill=True,
#         # capstyle='projecting', No clue what this is and the default gives error
#         # joinstyle=None
#     )
#
#     # Override defaults for histogram parameters if provided by user
#     if hist_kwargs is not None:
#         for key, value in hist_kwargs.iteritems():
#             default_hist_kwargs[key] = value
#
#     default_hist_kwargs['bins'] = np.linspace(x.min(), x.max(),
#                                               default_hist_kwargs['bins'])
#
#
#
#     ax.hist(x, **default_hist_kwargs)
#
#     # Set left frame attributes
#     ax.spines['bottom'].set_linewidth(1.0)
#     ax.spines['bottom'].set_color(text_and_line_color)
#
#     # Remove all but bottom frame line
#     ax.spines['right'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#     ax.spines['left'].set_visible(False)
#
#     # Remove ticks but not labels
#     ax.tick_params(axis=u'both', which=u'both',length=0)
#
#     # # Set x-tick label sizes and colors
#     # for x_tick in ax.xaxis.get_major_ticks():
#     #     x_tick.label.set_fontsize(small_text_size)
#     #     x_tick.label.set_color(text_and_line_color)
#     #
#     # # Set x-tick label sizes and colors
#     # for y_tick in ax.yaxis.get_major_ticks():
#     #     y_tick.label.set_fontsize(small_text_size)
#     #     y_tick.label.set_color(text_and_line_color)
#
#     ax.yaxis.grid(True,linestyle='--',linewidth=1)
#
# def plot_scatter():
#     """
#     """
#     pass
#
# def _get_feature_types(df):
#     """
#     Automatically determines suspected types of features and returns them in
#     a dictionary.
#     """
#     categorical_int_limit = 10
#
#     non_null_df = df
#
#     row_count = len(non_null_df)
#
#     feature_types = {}
#     for feature in non_null_df.columns:
#         unique_value_count = len(non_null_df[feature].unique())
#
#         if non_null_df[feature].dtype == int:
#             feature_type = 'int'
#         elif non_null_df[feature].dtype == float:
#             feature_type = 'float'
#         else:
#             feature_type = 'categorical'
#
#         if row_count == unique_value_count:
#             if feature_type in ['int', 'categorical']:
#                 feature_type = 'id'
#
#         if (feature_type is 'int'
#             and feature_type is not 'id'
#             and unique_value_count > 0
#             and unique_value_count <= categorical_int_limit):
#
#             feature_type = 'categorical_int'
#
#         if feature not in feature_types:
#             feature_types[feature] = feature_type
#         else:
#             raise Exception(
#                 "Feature, %s, is duplicated in dataframe."%(feature))
#
#     return feature_types
#
# def plot_single_distribution():
#     """
#     """
#     pass
#
# def compare_data(df, plot_vars=[], bar_alpha=0.85, bins=20, fig_size=16,
#                  fig_aspect=1, marker_size=2, marker_alpha=0.5,
#                  scatter_plot_filter=None, zoom=[], plot_medians=True):
#     """
#     Outputs a pairplot given a Pandas dataframe with these formats for
#     Row feature|Column feature combinations in either on- or off-diagonal
#     cells:
#
#     On-diagonal:
#         Categorical|Categorical:    Value counts of feature values ordered by
#                                     ascending value count and colored by
#                                     feature values
#         Numerical|Numerical:        Histogram of feature w/ no coloring (or by
#                                     desired label)
#     Off-diagonal:
#         Categorical|Categorical:    Stacked value count of row feature values
#                                     colored by column feature values
#         Categorical|Numerical:      Histograms of column feature for each row
#                                     feature value colored by row feature value
#         Numerical|Numerical:        Scatter plot of row feature values vs
#                                     column feature values w/ no coloring (or by
#                                     desired label)
#
#     """
#     # Initialize figure settings
#     figure_parameters = {
#         'row_count': [],
#         'col_count': [],
#         'fig_height': [],
#         'fig_width': []
#     }
#
#     # Encode plot type keyword arguments
#     plot_kwargs = {
#         'scatter': {
#             'linestyle': 'None',
#             'marker': 'o',
#             'markersize': marker_size,
#             'alpha': marker_alpha
#         },
#         'histogram': {
#             'alpha': bar_alpha
#         },
#         'bar': {
#             'alpha': bar_alpha,
#             'align': 'center'
#         }
#     }
#
#     # Set text and line color
#     grayLevel = 0.6
#     text_and_line_color = (0.0, 0.0, 0.0, grayLevel)
#
#     # Create axis keyword arguments
#     axis_kwargs = {}
#
#     # Set no x-tick, x-tick label, or y-tick generation as default for grid
#     # pair plots
#     if not zoom:
#         axis_kwargs['xticks'] = []
#         axis_kwargs['yticks'] = []
#         axis_kwargs['xticklabels'] = []
#
#     # Use all features if not explicitly provided by user
#     if not plot_vars:
#         plot_vars = list(df.columns)
#
#     # Dervive data types from dataframe
#     data_types = {}
#     for plot_var in plot_vars:
#         if df[plot_var].dtype.name == 'category':
#             data_types[plot_var] = 'category'
#         else:
#             data_types[plot_var] = 'numerical'
#
#     # Get number of features
#     feature_count = len(plot_vars)
#
#     # Derive orders and colors of each categorical feature value based on
#     # ascending value count
#     if scatter_plot_filter:
#         # Make sure the scatter plot filter is included
#         feature_list = list(set(plot_vars+[scatter_plot_filter]))
#     else:
#         feature_list = list(plot_vars)
#
#     feature_attributes = {}
#     for feature in feature_list:
#         # Get feature type
#         feature_type = data_types[feature]
#
#         # Initialize new features
#         if feature not in feature_attributes:
#             feature_attributes[feature] = {
#                 'feature_value_order': [],
#                 'feature_value_colors': {},
#                 'feature_value_counts': {}
#             }
#
#         # Get feature value order, value counts, and color for each value
#         if feature_type == 'category':
#             # Get feature value counts and sort in ascending order by count
#             sorted_value_count_df = df[feature].value_counts().sort_values(
#                                                                 ascending=True)
#
#             # Get feature values
#             sorted_feature_values = list(sorted_value_count_df.index.values)
#
#             # Save feature value counts for later
#             feature_attributes[feature]['feature_value_counts'] = \
#                 sorted_value_count_df.values
#
#             # Save feature value order (Ascending results in the colors I
#             # want yet not the right order, so I reverse them here)
#             feature_attributes[feature]['feature_value_order'] = \
#                 sorted_feature_values
#
#             # Get number of feature values
#             feature_value_count = len(sorted_feature_values)
#
#             # Generate colors for each feature value
#             for feature_value_ind,feature_value in enumerate(list(reversed(sorted_feature_values))):
#                 feature_attributes[feature]['feature_value_colors'][feature_value] = _get_color_val(feature_value_ind,feature_value_count)
#
#     # Generate figure settings
#     if not zoom:
#         figure_parameters['row_count'] = feature_count
#         figure_parameters['col_count'] = feature_count
#         figure_parameters['fig_height'] = fig_size
#         figure_parameters['fig_width'] = fig_size*fig_aspect
#     else:
#         figure_parameters['row_count'] = 1
#         figure_parameters['col_count'] = 1
#         figure_parameters['fig_height'] = fig_size
#         figure_parameters['fig_width'] = 0.5*fig_size
#
#     # Generate figure
#     fig = plt.figure(figsize=[figure_parameters['fig_height'],
#                               figure_parameters['fig_width']])
#
#     # Plot pair grid or single comparsion
#     if not zoom:
#         # Make sure there are no frames in the pair-grid plot
#         axis_kwargs['frame_on'] = False
#
#         # Graph pair grid
#         plot_pair_grid(df, fig, plot_vars=plot_vars, data_types=data_types,
#                        bar_alpha=bar_alpha, bins=bins,
#                        figure_parameters=figure_parameters,
#                        feature_attributes=feature_attributes,
#                        scatter_plot_filter=scatter_plot_filter,
#                        plot_kwargs=plot_kwargs,
#                        axis_kwargs=axis_kwargs,
#                        text_and_line_color=text_and_line_color)
#     else:
#         # Plot single graph
#         _plot_single_comparison(df,fig,features=zoom, data_types=data_types,
#                                figure_parameters=figure_parameters,
#                                feature_attributes=feature_attributes,
#                                plot_kwargs=plot_kwargs,
#                                axis_kwargs=axis_kwargs,
#                                text_and_line_color=text_and_line_color,
#                                plot_medians=plot_medians, bins=bins)
#
# def _plot_single_comparison(df, fig, features=[], data_types={},
#                             figure_parameters={}, feature_attributes={},
#                             plot_kwargs={}, axis_kwargs={},
#                             text_and_line_color=(), plot_medians=True,bins=20):
#     """
#     Plots a single cell of the pairgrid plot given a Pandas dataframe (df),
#     a list of the row-and column-features (features), a dictionary of feature
#     attributes (feature_attributes) containing the desired ordering/colors of
#     each value for a given feature, a dictionary of the data types (e.g.
#     'category' or 'numerical') for at least the provided features (data_types),
#     and a dictionary of figure parameters that includes the number of
#     rows/columns and the figure dimensions. This method is meant to be used
#     by the compare_data() method.
#     """
#     # Check input types and lengths
#     if not features or len(features) != 2 or type(features) is not list:
#         raise Exception('Keyword argument, features, must be present and \
#                         be a list of only 2 features.')
#
#     if not data_types:
#         raise Exception("A dictionary of data types ('category' or 'numerical'\
#                         must be present as the data_types keyword argument.")
#
#     # Get row and column features and types
#     row_feature = features[0]
#     col_feature = features[1]
#
#     # Check for their presence in the data types dictionary
#     if row_feature in data_types:
#         row_type = data_types[row_feature]
#     else:
#         raise Exception('Feature %s is not in the data_types keyword \
#                         argument'%(row_feature))
#
#     if col_feature in data_types:
#         col_type = data_types[col_feature]
#     else:
#         raise Exception('Feature %s is not in the data_types keyword \
#                         argument'%(col_feature))
#
#     # Get axis
#     ax = fig.add_subplot(1, 1, 1, **axis_kwargs)
#
#     # Choose plot type and plot
#     if row_type == 'category' and col_type == 'numerical':
#         unique_row_values = \
#             feature_attributes[row_feature]['feature_value_order']
#
#         colors = feature_attributes[row_feature]['feature_value_colors']
#
#         plot_label_vs_continuous(df, col_feature, row_feature,
#                                  output_labels=list(unique_row_values),
#                                  colors=colors, alpha=0.6,
#                                  figure_parameters=figure_parameters,
#                                  title=[], y_label=[], bins=bins,
#                                  plot_medians=plot_medians,
#                                  plot_quantiles=False,
#                                  text_and_line_color=text_and_line_color)
#
#     elif row_type == 'numerical' and col_type == 'category':
#         raise Exception("The first feature of the zoom keyword argument is " \
#                         "numerical and the 2nd is categorical. There are no " \
#                         "current plans to support this type of plot.")
#     elif row_type == 'category' and col_type == 'category':
#         unique_col_values = \
#             feature_attributes[col_feature]['feature_value_order']
#
#         colors = \
#             [feature_attributes[col_feature]['feature_value_colors'][col_value] \
#                 for col_value in unique_col_values]
#
#         plot_label_versus_label(df, ax, features[0], features[1],
#                                 output_labels=list(unique_col_values),
#                                 colors=colors, alpha=0.6,
#                                 figure_parameters=figure_parameters,
#                                 x_label=[], title=[],
#                                 feature_attributes=feature_attributes,
#                                 plot_kwargs=plot_kwargs, bar_edge_color='w',
#                                 text_and_line_color=text_and_line_color)
#     elif row_type == 'numerical' and col_type == 'numerical':
#         raise NameError("For the moment, numerical vs numerical can't be " \
#                         "plotted")
#     else:
#         raise NameError('Logic error involving single plot and feature types')
#
#
# def plot_pair_grid(df, fig, plot_vars=[], data_types=[], bar_alpha=0.85,
#                    bins=20, dpi=[], figure_parameters=[], #fig_size=12,fig_aspect=1,
#                    scatter_plot_filter=None, feature_attributes={},
#                    plot_kwargs={}, axis_kwargs={}, text_and_line_color=()):
#
#     # Move first categorical feature to front column in front of a first
#     # numerical feature
#     feature_types = [data_types[feature] for feature in plot_vars]
#     if 'category' in feature_types and feature_types[0]=='numerical':
#         # Pop out first categorical variable
#         feature_to_move = plot_vars.pop(feature_types.index('category'))
#
#         # Issue warning to user
#         print "WARNING: Due to a y-tick label bug I can't seem to overcome, " \
#               "the first continuous feature encountered in either the " \
#               "dataframe column list or the user-specified list of features " \
#               "keyword argument, plot_vars, %s has been moved to the front " \
#               "of the list because the first " \
#               "feature, %s, is numerical.\n" %(feature_to_move,plot_vars[0])
#
#         # Move first categorical feature to the front of the list of features
#         plot_vars.insert(0,feature_to_move)
#
#     # Count number of features
#     number_features = len(plot_vars)
#
#     # Raise error if the desired feature to color the scatter plots isn't found and/or is not categorical
#     if scatter_plot_filter:
#         if scatter_plot_filter not in df.columns:
#             raise Exception("The scatter_plot_filter keyword argument, %s, " \
#                             "is not one of the features."%(scatter_plot_filter))
#
#         if data_types[scatter_plot_filter] != 'category':
#             raise Exception("The scatter_plot_filter keyword argument, %s, " \
#                             "is not defined as a category in the data_types " \
#                             "keyword argument. Only categorical features " \
#                             "can be used " \
#                             "to color scatter plots."%(scatter_plot_filter))
#
#     # Set default text font, color, and size
#     text_family = 'sans-serif'
#     text_font = 'Helvetica Neue Light'
#     text_font_size = 12
#     tick_label_size = text_font_size-3
#
#     text_properties = {
#         'tick_labels': {
#             'family': 'sans-serif',
#             'weight': 'normal',
#             'size': tick_label_size
#         }
#     }
#
#     # Set padding of axis labels so they don't overlap with tick-labels
#     label_padding = 0.65
#
#     # Set bar parameters
#     bar_edge_color = 'w'
#
#     # Set bar_edge_color as default if provided by user
#     if bar_edge_color:
#         plot_kwargs['histogram']['edgecolor'] = bar_edge_color
#         plot_kwargs['bar']['edgecolor'] = bar_edge_color
#
#     # Graph axes
#     for axis_row_ind in range(number_features):
#         # Get the row feature and its type
#         row_feature = plot_vars[axis_row_ind]
#         row_type = data_types[row_feature]
#
#         # Initialize current row of axes
#         for axis_column_ind in range(number_features):
#             # Get the column feature and its type
#             col_feature = plot_vars[axis_column_ind]
#             col_type = data_types[col_feature]
#
#             # Determine if this is a diagonal, left-edge, and/or
#             # bottom-edge grid cell
#             diagonal_flag = False
#             left_edge_flag = False
#             bottom_edge_flag = False
#             if axis_row_ind == axis_column_ind:
#                 diagonal_flag = True
#
#             if axis_column_ind == 0:
#                 left_edge_flag = True
#
#             if axis_row_ind == number_features-1:
#                 bottom_edge_flag = True
#
#             # Determine plot type
#             if row_type == 'numerical' and col_type == 'numerical':
#                 if diagonal_flag:
#                     plot_type = 'histogram'
#                 else:
#                     plot_type = 'scatter'
#             elif row_type == 'category' and col_type == 'numerical':
#                 plot_type = 'histogram'
#             elif row_type == 'category' and col_type == 'category':
#                 plot_type = 'bar'
#             elif row_type == 'numerical' and col_type == 'category':
#                 plot_type = None
#             else:
#                 raise Exception("Logic error invovling plot types encountered.")
#
#             # Set axis index
#             axis_ind = axis_row_ind*number_features+axis_column_ind+1
#
#             # Add axis subplot
#             if plot_type or left_edge_flag or bottom_edge_flag:
#                 ax = fig.add_subplot(figure_parameters['row_count'],
#                                      figure_parameters['col_count'],
#                                      axis_ind,**axis_kwargs)
#
#             # Generate plot in axis
#             graph_subplot(ax, df, col_feature, row_feature, feature_attributes,
#                           plot_type=plot_type,
#                           scatter_plot_filter=scatter_plot_filter,
#                           plot_kwargs=plot_kwargs, diagonal_flag=diagonal_flag,
#                           bins=bins, bar_edge_color=bar_edge_color,
#                           left_edge_flag=left_edge_flag,
#                           tick_label_size=tick_label_size,
#                           text_and_line_color=text_and_line_color)
#
#             # Set y- and x-axis labels
#             if left_edge_flag:
#                 ax.set_ylabel(row_feature, color=text_and_line_color,
#                               size=text_font_size)
#                 ax.get_yaxis().set_label_coords(-label_padding, 0.5)
#             if bottom_edge_flag:
#                 ax.set_xlabel(col_feature, color=text_and_line_color,
#                               size=text_font_size)
#
#             # Set y-axis tick labels if on left
#             if left_edge_flag:
#                 ax.set_yticklabels(ax.get_yticklabels(),
#                                    text_properties['tick_labels'])
#
# def graph_subplot(ax,df,col_feature,row_feature,feature_attributes,
#                   plot_type=[],plot_kwargs=[],scatter_plot_filter=[],
#                   diagonal_flag=[],bins=20,bar_edge_color=[],
#                   left_edge_flag=[],tick_label_size=[],text_and_line_color=()):
#     """
#     Plots subplot given the axis object, dataframe, row- and column- feature
#     names,
#     """
#     if plot_type == 'scatter':
#         # Get data
#         x = df[col_feature].values
#         y = df[row_feature].values
#
#         # Plot scatter plot either labeled or unlabeled
#         if not scatter_plot_filter:
#             # Pick color
#             plot_kwargs['scatter']['markerfacecolor'] = _get_color_val(0,1)
#
#             ax.plot(x,y,**plot_kwargs['scatter'])
#         else:
#             # Plot separate datasets
#             for feature_value in \
#                 feature_attributes[scatter_plot_filter]['feature_value_order']:
#                 # Get data
#                 x = df[col_feature][df[scatter_plot_filter]==feature_value]
#                 y = df[row_feature][df[scatter_plot_filter]==feature_value]
#
#                 # Get color
#                 color = \
#                     feature_attributes[scatter_plot_filter]['feature_value_colors'][feature_value]
#
#                 plot_kwargs['scatter']['markerfacecolor'] = color
#
#                 # Plot scatter plot for current data
#                 ax.plot(x,y,**plot_kwargs['scatter'])
#
#     elif plot_type == 'histogram':
#         # Plot histogram of data based on type of plot and whether on- or off-diagonal
#         if diagonal_flag:
#             # Get data
#             x = df[row_feature].values
#
#             # Generate bins based on minimum and maximum and number of bars
#             bins = np.linspace(df[row_feature].min(),df[row_feature].max(),bins)
#
#             # Pick color
#             color = _get_color_val(0,1)
#
#             # Set series-specific parameters
#             ## Set lower value to start bars from
#             plot_kwargs[plot_type]['bins'] = bins
#
#             ## Set series label
#             plot_kwargs[plot_type]['label'] = row_feature
#
#             ## Set bar colors
#             plot_kwargs[plot_type]['color'] = color
#
#             ## Set bar edge color (default is color of current bar unless provided by user)
#             if not bar_edge_color:
#                 plot_kwargs[plot_type]['edgecolor'] = color
#
#             # Plot histogram
#             ax.hist(x,**plot_kwargs[plot_type])
#         else:
#             # Get unique category values
#             unique_row_feature_values = feature_attributes[row_feature]['feature_value_order']
#
#             # Generate bins based on minimum and maximum and number of bars
#             bins = np.linspace(df[col_feature].min(),df[col_feature].max(),bins)
#
#             # Plot a histogram for the column-feature for each row-feature value
#             for unique_feature_value in unique_row_feature_values:
#                 # Obtain color of current histogram
#                 color = feature_attributes[row_feature]['feature_value_colors'][unique_feature_value]
#
#                 # Get data for current histogram
#                 data = df[col_feature][df[row_feature]==unique_feature_value].values
#
#                 # Set series-specific parameters
#                 ## Set lower value to start bars from
#                 plot_kwargs[plot_type]['bins'] = bins
#
#                 ## Set series label
#                 plot_kwargs[plot_type]['label'] = unique_row_feature_values
#
#                 ## Set bar colors
#                 plot_kwargs[plot_type]['color'] = color
#
#                 ## Set bar edge color (default is color of current bar unless provided by user)
#                 if not bar_edge_color:
#                     plot_kwargs[plot_type]['edgecolor'] = color
#
#                 # Plot current histogram
#                 ax.hist(data,**plot_kwargs[plot_type])
#
#             # Make all bars in multiple overlapping histogram plot visible
#             ## Get number of histograms
#             histogram_count = len(unique_row_feature_values)
#
#             ## Collect Patch objects representing bars at the same position
#             bars = {}
#             for bar in ax.patches:
#                 # Get current bar position
#                 bar_position = bar.get_x()
#
#                 # Initialize x-position list in bar dictionary if not present
#                 if bar_position not in bars:
#                     bars[bar_position] = []
#
#                 # Add current bar to collection of bars at that position
#                 bars[bar_position].append(bar)
#
#             ## Sort bars based on height so smallest is visible
#             for bar_position, bar_group in bars.iteritems():
#                 # Sort bars by height order for current bar group at current position
#                 if len(bar_group) > 1:
#                     # Sort by height
#                     bar_group = sorted(bar_group, key=lambda x: x.get_height(),reverse=True)
#
#                     # Set layer position to current order
#                     for bar_ind,bar in enumerate(bar_group):
#                         bar.set_zorder(bar_ind)
#
#     elif plot_type == 'bar':
#         # Get row feature values and counts sorted by ascending counts
#         sorted_row_values = feature_attributes[row_feature]['feature_value_order']
#         sorted_row_value_counts = feature_attributes[row_feature]['feature_value_counts']
#
#         # Set tick-labels
#         tick_labels = sorted_row_values
#
#         # Set bar and tick-label positions
#         bar_positions = np.arange(len(sorted_row_values))
#
#         # Draw bar chart based on whether on- or off-diagonal
#         if diagonal_flag:
#             # Pick color
#             color = _get_color_val(0,1) # Just pick first color
#
#             # Set series-specific parameters
#             ## Set lower value to start bars from
#             plot_kwargs[plot_type]['left'] = 0
#
#             ## Set bar colors
#             plot_kwargs[plot_type]['color'] = color
#
#             ## Set bar edge color (default is color of current bar unless provided by user)
#             if not bar_edge_color:
#                 plot_kwargs[plot_type]['edgecolor'] = color
#
#             # Draw bar plot
#             bars = ax.barh(bar_positions,sorted_row_value_counts,**plot_kwargs[plot_type])
#
#             # Set each bar as the color corresponding to each row feature value
#             for sorted_row_value_ind,sorted_row_value in enumerate(sorted_row_values):
#                 bar_color = feature_attributes[row_feature]['feature_value_colors'][sorted_row_value]
#
#                 bars[sorted_row_value_ind].set_color(bar_color)
#
#                 if not bar_edge_color:
#                     bars[sorted_row_value_ind].set_edgecolor(bar_color)
#                 else:
#                     bars[sorted_row_value_ind].set_edgecolor(bar_edge_color)
#
#                 bars[sorted_row_value_ind].set_label(sorted_row_value)
#         else:
#             # Obtain column feature
#             unique_col_feature_values = feature_attributes[col_feature]['feature_value_order']
#
#             # Get the row feature count data for each value of the column feature and sort in descending order
#             split_data = {}
#             for unique_col_feature_value in unique_col_feature_values:
#                 # Find and save data of row feature with current value of column feature,
#                 # count the number of each row feature value, and sort by the order
#                 # determined by the total count of each row feature value
#                 sorted_filtered_data = df[row_feature][df[col_feature]==unique_col_feature_value].value_counts().loc[sorted_row_values]
#
#                 # Fill N/A values with zero
#                 sorted_filtered_data.fillna(0,inplace=True)
#
#                 # Add data to dictionary
#                 split_data[str(unique_col_feature_value)] = sorted_filtered_data.values
#
#             # Initalize value for bottom bar for stacked bar charts
#             bottom_bar_buffer = np.zeros(len(sorted_row_values))
#
#             # Plot stacked bars for row feature data corresponding to each column feature value
#             for unique_col_feature_value_ind,unique_col_feature_value in enumerate(unique_col_feature_values):
#                 # Get color for bars
#                 color = feature_attributes[col_feature]['feature_value_colors'][unique_col_feature_value]
#
#                 # Get data for current col_feature value and column_feature
#                 data = split_data[str(unique_col_feature_value)]
#
#                 # Add previous values to current buffer
#                 if unique_col_feature_value_ind:
#                     previous_feature_value = unique_col_feature_values[unique_col_feature_value_ind-1]
#
#                     bottom_bar_buffer = bottom_bar_buffer + split_data[str(previous_feature_value)]
#
#                 # Set series-specific parameters
#                 ## Set lower value to start bars from
#                 plot_kwargs[plot_type]['left'] = bottom_bar_buffer
#
#                 # Set bar colors
#                 plot_kwargs[plot_type]['color'] = color
#
#                 ## Set bar edge color (default is color of current bar unless provided by user)
#                 if not bar_edge_color:
#                     plot_kwargs[plot_type]['edgecolor'] = color
#
#                 # Plot bars corresponding to current series
#                 ax.barh(bar_positions,data,**plot_kwargs[plot_type])
#
#         # Set y-tick positions and labels if against left-side
#         if left_edge_flag:
#             ax.set_yticks(bar_positions)
#             ax.set_yticklabels(tick_labels,size=tick_label_size,color=text_and_line_color)
#
# def plot_label_vs_continuous(df,input_feature,output_label_feature,output_labels=[],
#                             colors=[],alpha=0.6,figure_parameters={},title=[],y_label=[],
#                             bins=20,plot_medians=True,plot_quantiles=False,text_and_line_color=()):
#     """
#     Plots the distributions of the input_feature for each output_label_feature value
#     """
#     # Form automatic title if not provided
#     if not title:
#         title = '%s distributions by %s labels'%(input_feature,output_label_feature)
#
#     # Set font attributes
#     large_text_size = 14
#     small_text_size = 12
#
#     # Set axis/legend labels
#     if y_label:
#         y_label = output_label_feature
#     else:
#         y_label = 'Frequency'
#     x_label = input_feature
#
#     # Obtain unique output label feature values
#     unique_output_label_feature_values = df[output_label_feature].value_counts().sort_index().index.values
#
#     # Set bin bounds for cleaner plots
#     bins = np.linspace(df[input_feature].min(),df[input_feature].max(),bins)
#
#     # Plot data
#     cmap = matplotlib.cm.autumn
#     axes = []
#     lines = []
#     for unique_output_label_feature_value_ind,unique_output_label_feature_value in enumerate(unique_output_label_feature_values):
#         # Obtain current data
#         current_distribution = df[input_feature][df[output_label_feature]==unique_output_label_feature_value]
#
#         # Set series color
#         if colors:
#             series_color = colors[unique_output_label_feature_value]
#         else:
#             series_color = cmap(unique_output_label_feature_value_ind)
#
#         # Plot histogram and save axis
#         axes.append(current_distribution.plot(kind='hist',color=series_color,
#                                               alpha=alpha,
#                                               figsize=[figure_parameters['fig_height'],
#                                                        figure_parameters['fig_width']],
#                                               bins=bins))
#
#     # Obtain data handles for use in legend
#     h,_ = axes[-1].get_legend_handles_labels()
#
#     # Plot median lines if desired
#     if plot_medians:
#         for unique_output_label_feature_value_ind,unique_output_label_feature_value in enumerate(unique_output_label_feature_values):
#             # Obtain current data
#             current_distribution = df[input_feature][df[output_label_feature]==unique_output_label_feature_value]
#
#             # Set series color
#             if colors:
#                 series_color = colors[unique_output_label_feature_value]
#             else:
#                 series_color = cmap(unique_output_label_feature_value_ind)
#
#             # Plot median lines to histograms in diagonals if specified
#             axes[-1].axvline(current_distribution.median(),alpha=0.9,color=series_color)
#
#     # Plot 0, 25, 75, and 100% quartiles if desired
#     if plot_quantiles:
#         for unique_output_label_feature_value_ind,unique_output_label_feature_value in enumerate(unique_output_label_feature_values):
#             # Obtain current data
#             current_distribution = df[input_feature][df[output_label_feature]==unique_output_label_feature_value]
#
#             # Set series color
#             if colors:
#                 series_color = colors[unique_output_label_feature_value_ind]
#             else:
#                 series_color = cmap(unique_output_label_feature_value_ind)
#
#             # Plot median lines to histograms in diagonals if specified
#             axes[-1].axvline(current_distribution.quantile(0.25),alpha=0.5,label=unique_output_label_feature_value,color=series_color,linestyle='--')
#             axes[-1].axvline(current_distribution.quantile(0.75),alpha=0.5,label=unique_output_label_feature_value,color=series_color,linestyle='--')
#             axes[-1].axvline(current_distribution.quantile(0.0),alpha=0.25,label=unique_output_label_feature_value,color=series_color,linestyle='--')
#             axes[-1].axvline(current_distribution.quantile(1.0),alpha=0.25,label=unique_output_label_feature_value,color=series_color,linestyle='--')
#
#     # Set title, x and y labels, and legend values
#     plt.title(title,size=large_text_size)
#
#     # Place x- and y-labels
#     plt.xlabel(x_label,size=small_text_size)
#     plt.ylabel(y_label,size=small_text_size)
#
#     # Place legend
#     if output_labels:
#         unique_output_label_feature_values
#         legend_labels = output_labels
#         plt.legend(h,unique_output_label_feature_values,loc='center left',bbox_to_anchor=(1, 0.5))
#     else:
#         plt.legend(loc='right',bbox_to_anchor=(1, 0.5))
#
#     # Modify plot limits so last gridline visible
#     ax = axes[0]
#     yticks, yticklabels = plt.yticks()
#     ymin = yticks[0] #(3*xticks[0] - xticks[1])/2.
#     ymax = 1.1*(3*yticks[-1]-yticks[-2])/2.
#     ax.set_ylim(ymin, ymax)
#
#     # Set left frame attributes
#     ax.spines['bottom'].set_linewidth(1.0)
#     ax.spines['bottom'].set_color(text_and_line_color)
#
#     # Remove all but bottom frame line
#     ax.spines['right'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#     ax.spines['left'].set_visible(False)
#
#     # Add grid
#     ax.yaxis.grid(True,linestyle='--',linewidth=1)
#
#     # Place smallest bars in front
#     ## loop through all patch objects and collect ones at same x
#
#     ## Obtain number of unique data series
#     num_lines = len(unique_output_label_feature_values)
#
#     ## Create dictionary of lists containg patch objects at the same x-postion
#     patch_dict = {}
#     for patch in ax.patches:
#         # Get current patch position
#         patch_x_position = patch.get_x()
#
#         # Initialize x-position list in patch dictionary if not present
#         if patch_x_position not in patch_dict:
#             patch_dict[patch_x_position] = []
#
#         # Add dictionary object
#         patch_dict[patch_x_position].append(patch)
#
#     ## loop through sort assign z-order based on sort
#     for x_pos, patches in patch_dict.iteritems():
#         # Check that there is more than one patch
#         if len(patches) == 1:
#             continue
#
#         # Sort patches
#         patches.sort(cmp=patch_height_sort)
#
#         # Set order of patches
#         for patch in patches:
#             patch.set_zorder(patches.index(patch)+num_lines)
#
#     # Show plot
#     plt.show()
#
# def patch_height_sort(patch_one,patch_two):
#     """
#     Returns 1 flag if second patch higher
#     """
#     if patch_two.get_height() > patch_one.get_height():
#         return 1
#     else:
#         return -1
#
# def plot_label_versus_label(df,ax,data_feature,hue_feature,output_labels=[],
#                             colors=[],alpha=0.6,figure_parameters={},x_label=[],title=[],
#                             feature_attributes={},plot_kwargs={},bar_edge_color='w',
#                             text_and_line_color=()):
#     # Form automatic title if not provided
#     if not title:
#         title = 'Proportations of '+hue_feature+' category within '+data_feature+' populations'
#
#     # Set plot_type
#     plot_type = 'bar'
#
#     # Set font attributes
#     large_text_size = 14
#     small_text_size = 12
#
#     # Set axis/legend labels
#     y_label = data_feature
#     if not x_label:
#         x_label = 'Frequency'
#
#     # Form pivot table between input and output label features
#     label_by_label = df[[data_feature, hue_feature]].pivot_table(
#         columns=[hue_feature],
#         index=[data_feature],
#         aggfunc=len)
#
#     # Order by specific data feature value
#     label_by_label = label_by_label.loc[feature_attributes[data_feature]['feature_value_order']]
#
#     # Fill in N/A values with zero
#     label_by_label.fillna(0,inplace=True)
#
#     # Obtain column feature
#     unique_col_feature_values = feature_attributes[hue_feature]['feature_value_order']
#
#     # Initalize value for bottom bar for stacked bar charts
#     sorted_row_values = feature_attributes[data_feature]['feature_value_order']
#     bottom_bar_buffer = np.zeros(len(sorted_row_values))
#
#     # Set tick-labels
#     tick_labels = sorted_row_values
#
#     # Set bar and tick-label positions
#     bar_positions = np.arange(len(sorted_row_values))
#
#     # Plot stacked bars for row feature data corresponding to each column feature value
#     for unique_col_feature_value_ind,unique_col_feature_value in enumerate(unique_col_feature_values):
#         # Get color for bars
#         color = feature_attributes[hue_feature]['feature_value_colors'][unique_col_feature_value]
#
#         # Get data for current col_feature value and column_feature
#         data = label_by_label[unique_col_feature_value]
#
#         # Add previous values to current buffer
#         if unique_col_feature_value_ind:
#             previous_feature_value = unique_col_feature_values[unique_col_feature_value_ind-1]
#
#             bottom_bar_buffer = bottom_bar_buffer + label_by_label[previous_feature_value]
#
#         # Set series-specific parameters
#         ## Set lower value to start bars from
#         plot_kwargs[plot_type]['left'] = bottom_bar_buffer
#
#         # Set bar colors
#         plot_kwargs[plot_type]['color'] = color
#
#         ## Set bar edge color (default is color of current bar unless provided by user)
#         if not bar_edge_color:
#             plot_kwargs[plot_type]['edgecolor'] = color
#
#         # Plot bars corresponding to current series
#         ax.barh(bar_positions,data,**plot_kwargs[plot_type])
#
#     # Modify horizontal plot limits so last gridline visible on x-axis
#     x_ticks = ax.get_xticks()
#
#     x_min = x_ticks[0] #(3*xticks[0] - xticks[1])/2.
#     x_max = (3*x_ticks[-1]-x_ticks[-2])/2.
#
#     ax.set_xlim(x_min,x_max)
#
#     # Modify vertical plot limits so there's a bit of padding on the y-axis
#     yticks = ax.get_yticks()
#
#     ymin = (3*yticks[0]-yticks[1])/2.
#     ymax = (3*yticks[-1]-yticks[-2])/2.
#
#     ax.set_ylim(ymin, ymax)
#
#     # Set x-tick label sizes and colors
#     for x_tick in ax.xaxis.get_major_ticks():
#         x_tick.label.set_fontsize(small_text_size)
#         x_tick.label.set_color(text_and_line_color)
#
#     # Set y-tick positions and labels
#     ax.set_yticks(bar_positions)
#     ax.set_yticklabels(tick_labels,size=small_text_size,color=text_and_line_color)
#
#     # Set title, x and y labels, and legend values
#     ax.set_title(title,size=large_text_size,color=text_and_line_color)
#
#     ax.set_xlabel(x_label,color=text_and_line_color,size=small_text_size)
#     ax.set_ylabel(y_label,color=text_and_line_color,size=small_text_size)
#
#     if output_labels:
#         legend_labels = output_labels
#         plt.legend(legend_labels,loc='right',bbox_to_anchor=(1.05, 0.5))
#     else:
#         plt.legend(loc='right',bbox_to_anchor=(1.05, 0.5))
#
#     # Set left frame attributes
#     ax.spines['right'].set_visible(True)
#     ax.spines['left'].set_linewidth(1.0)
#     ax.spines['left'].set_color(text_and_line_color)
#
#     # Remove all but frame line
#     ax.spines['right'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#
#     # Add grid
#     ax.xaxis.grid(True,linestyle='--',linewidth=1)
#
#     # Hide the right and top spines
#     plt.show()
#
#     def get_step_colors(self, df, color_by=None, color_map='viridis'):
#         """
#         """
#         ######### Collect pipeline indices with desired attribute  #########
#         step_colors = self.get_organized_pipelines(step_type=color_by)
#
#         ############### Build working/indexible colormap ###############
#         color_count = len(step_colors.keys())
#
#         cmap = mpl_plt.get_cmap(color_map)
#
#         cNorm = mpl_colors.Normalize(vmin=0, vmax=color_count-1)
#
#         scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cmap)
#
#         sorted_steps = sorted(step_colors.keys(), key=self.order_by_parameter)
#
#         # Set internal colors
#         color_ind = 0
#         for step_name in sorted_steps:
#             step = step_colors[step_name]
#
#             if step_name == 'None':
#                 step['color'] = 'k'
#             else:
#                 step['color'] = scalarMap.to_rgba(color_ind)
#
#                 color_ind += 1
#
#         return step_colors
#
# def _get_color_val(color_ind, color_count, color_map='jet'):
#     if color_map == 'custom':
#         scalar_map = ['gray', 'cyan', 'orange', 'magenta', 'lime', 'red',
#                       'purple', 'blue', 'yellow', 'black']
#     else:
#         cmap = mpl_plt.get_cmap(color_map)
#
#         cNorm = mpl_colors.Normalize(vmin=0, vmax=color_count-1)
#
#         scalar_map = cmx.ScalarMappable(norm=cNorm, cmap=cmap)
#
#     if color_map != 'custom':
#         if not color_ind:
#             color = 'gray'
#         else:
#             color = scalar_map.to_rgba(color_ind)
#     else:
#         color = scalar_map[color_ind]
#
#     return color
#
#
#
#
#
#
#     # colormap = 'viridis'
#     # color_map = plt.get_cmap(colormap)
#     #
#     # custom_map = ['gray','cyan','orange','magenta','lime','red','purple','blue','yellow','black']
#     #
#     # # Choose color
#     # if num_series > len(custom_map):
#     #     if not ind:
#     #         color = 'gray'
#     #     else:
#     #         if num_series != 1:
#     #             color = color_map(float(ind)/(float(num_series)-1))
#     #         else:
#     #             color = color_map(float(ind)/(float(num_series)))
#     #
#     # else:
#     #     color = custom_map[ind]
#     #
#     # return color
