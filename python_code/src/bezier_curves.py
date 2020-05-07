from abc import ABCMeta, abstractmethod


class Segment(metaclass=ABCMeta):

    @property
    @abstractmethod
    def control_points(self):
        pass

    @abstractmethod
    def point_at(self, t):
        pass

    @abstractmethod
    def sub_segment(self, t):
        pass


class Line(Segment):

    def __init__(self, *coords):
        self._control_points = coords[:4]

    @property
    def control_points(self):
        return self._control_points

    def point_at(self, t):
        x0, y0, x1, y1 = self._control_points
        return x0 * (1 - t) + x1 * t, y0 * (1 - t) + y1 * t

    def sub_segment(self, t):
        x0, y0 = self._control_points[:2]
        xm, ym = self.point_at(t)
        return Line(x0, y0, xm, ym)

    def __repr__(self):
        return "Line(%f, %f, %f, %f)" % self.control_points


class Quad(Segment):

    def __init__(self, *coords):
        self._control_points = coords[:6]
        self.line = Line(*coords[:4])

    @property
    def control_points(self):
        return self._control_points

    def point_at(self, t):
        x0, y0, x1, y1, x2, y2 = self._control_points
        u = 1 - t
        uu, ut, tt = u * u, u * t, t * t
        return x0 * uu + x1 * 2 * ut + x2 * tt, \
               y0 * uu + y1 * 2 * ut + y2 * tt

    def sub_segment(self, t):
        x0, y0 = self._control_points[:2]
        xm, ym = self.line.point_at(t)
        xq, yq = self.point_at(t)
        return Quad(x0, y0, xm, ym, xq, yq)

    def __repr__(self):
        return "Quad(%f, %f, %f, %f, %f, %f)" % self.control_points


class Cubic(Segment):

    def __init__(self, *coords):
        self._control_points = coords[:8]
        self.line = Line(*coords[:4])
        self.quad = Quad(*coords[:6])

    @property
    def control_points(self):
        return self._control_points

    def point_at(self, t):
        x0, y0, x1, y1, x2, y2, x3, y3 = self._control_points
        u = 1 - t
        uu, tt = u * u, t * t
        uuu, uut, utt, ttt = uu * u, uu * t, u * tt, t * tt
        return x0 * uuu + x1 * 3 * uut + x2 * 3 * utt + x3 * ttt,\
               y0 * uuu + y1 * 3 * uut + y2 * 3 * utt + y3 * ttt

    def sub_segment(self, t):
        x0, y0 = self._control_points[:2]
        xm, ym = self.line.point_at(t)
        xq, yq = self.quad.point_at(t)
        xc, yc = self.point_at(t)
        return Cubic(x0, y0, xm, ym, xq, yq, xc, yc)

    def __repr__(self):
        return "Cubic(%f, %f, %f, %f, %f, %f, %f, %f)" % self.control_points
