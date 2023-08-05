from sfsimodels import output as mo
from collections import OrderedDict

import matplotlib
import matplotlib.font_manager as font_manager

from matplotlib import rc
rc('font', family='Times New Roman', size=10)
font_prop = font_manager.FontProperties(size=9, family='serif')  # , family='serif'

matplotlib.rcParams['lines.linewidth'] = 0.8


def save_and_latex_figure(up, figure, name, save=1, extension=""):
    """
    Saves a figure and produces python output.
    :param figure:
    :param name:
    :param save: =1 temporary save, =2, for publication
    :return:
    """
    figure.tight_layout()
    ftype = ".png"
    if save == 1:
        figure.savefig("/temp_output/" + name + ftype, dpi=150)
    else:
        figure.savefig(up.PUBLICATION_FIGURE_PATH + name + extension + ftype, dpi=400)
    para = ""
    para += "\\begin{figure}[H]\n"
    para += "\centering\n"
    para += "\\includegraphics{%s/%s%s}\n" % (up.FIGURE_FOLDER, name, ftype)
    para += "\\caption{%s \label{fig: %s}}\n" % (name.replace("_", " "), name)
    para += "\\end{figure}\n"
    return para


def output_to_table(**kwargs):
    mo.output_to_table(**kwargs)


def add_table_ends(**kwargs):
    mo.add_table_ends(**kwargs)


def get_file_name_for_build_results(python_name):
    name = python_name.replace('.py', '')
    name = name.split("figure_")[-1]
    name = "fig_results_" + name + ".txt"
    return name


def unpack_build_results(python_name, titles):
    res_fpath = get_file_name_for_build_results(python_name)
    res_file = open(res_fpath)
    res_lines = res_file.readlines()
    data = OrderedDict()
    for line in res_lines:
        # name, sd_start, sd_end, period, max_disp_time
        items = line.split(",")
        if items[0] not in data:
            data[items[0]] = OrderedDict()
            for i in range(len(items)):
                data[items[0]][titles[i]] = []

        for i in range(len(items)):
            try:
                data[items[0]][titles[i]].append(float(items[i]))
            except ValueError:
                data[items[0]][titles[i]].append(items[i])
    return data

