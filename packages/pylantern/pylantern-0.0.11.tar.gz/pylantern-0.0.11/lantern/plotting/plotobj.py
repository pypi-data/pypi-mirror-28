from abc import abstractmethod, ABCMeta


class BasePlot(metaclass=ABCMeta):
    def __init__(self, backend):
        pass

    @abstractmethod
    def show(self, title='', xlabel='', ylabel='', xaxis=True, yaxis=True, xticks=True, yticks=True, legend=True, grid=True, **kwargs):
        pass

    @abstractmethod
    def area(self, data, color=None, y_axis='left', stacked=False, **kwargs):
        pass

    @abstractmethod
    def bar(self, data, color=None, y_axis='left', stacked=False, **kwargs):
        pass

    @abstractmethod
    def line(self, data, color=None, y_axis='left', **kwargs):
        pass

    @abstractmethod
    def scatter(self, data, color=None, x=None, y=None,  y_axis='left', **kwargs):
        pass

    @abstractmethod
    def step(self, data, color=None, y_axis='left', **kwargs):
        pass
