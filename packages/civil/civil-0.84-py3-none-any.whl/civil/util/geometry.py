# coding=utf-8
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

"""


class line2d:
    """


 """

    def __init__(self, a, b, c):
        """
        line ax+by=c 
        normalize xco to 1, unless it's zero, then normalize yco 
        if a and b are zero, we don't handle the error.
 """

        if a == 0:
            self.xco = 0
            self.yco = 1
            self.constant = c / b
        else:
            self.xco = 1
            self.yco = b / a
            self.constant = c / a

    def intersect(self, them):
        """
        Intersection of two lines.  We could also do this with the matrix
        class, but this specialized code is already written, and probably faster anyway.
        """
        # are we parallel? 
        if self.yco == them.yco:
            # we are. We'll give correct answer, more or less
            if self.constant == them.constant:
                return ()  # same line! should return self instead?
            else:
                return ()  # ditto.
        # ok, not parallel .
        if self.xco != 0 and them.xco != 0:  # ok, neither is horizontal.
            Yintersect = (self.constant - them.constant) / (self.yco - them.yco)
            Xintersect = self.constant - self.yco * Yintersect
        elif self.xco == 0:  # self horizontal
            Yintersect = self.constant  # yco is 1, remember
            Xintersect = them.constant - them.yco * Yintersect
        elif them.xco == 0:  # them horizontal
            Yintersect = them.constant
            Xintersect = self.constant - self.yco * Yintersect
        else:
            raise RuntimeError("Invalid lines.")

        return Xintersect, Yintersect

    def hasPoint(self, P):
        """

        Args:
            P: 

        Returns:

        """
        if (self.xco * P[0] + self.yco * P[1]) == self.constant:
            return 1
        else:
            return 0

    def __repr__(self):
        return "%dx + %dy = %d" % (self.xco, self.yco, self.constant)


class matrix:
    """
    Not really full or proper matrix implementation, just
    enough to solve systems of linear equations.

    No doubt it's full of bugs and for that matter spelling errors,
    but it does seem to work for the relevent cases.
    """

    def __init__(self, input):
        self.m = input
        # input should be a list of lists of floats, all same length
        return

    def positivise(self):
        """
        make sure first column is all non-negative.
        Otherwise, sort won't do what we want.
        """
        for row in self.m:
            if row[0] < 0:
                for index in range(len(row)):
                    row[index] *= -1.0

    def reduceColumn(self):
        """

        Returns:

        """
        self.positivise()
        self.m.sort()
        self.m.reverse()
        if len(self.m) == 1 or self.m[0][0] == 0:
            return self.m  # degenerate case
        for row in range(1, len(self.m)):
            factor = (self.m[row][0]) / ((self.m[0][0]) * 1.0)  # coerce factor to be a float
            for column in range(len(self.m[row])):
                self.m[row][column] = self.m[row][column] - (self.m[0][column] * factor)
        return

    def subMatrix(self):
        """
        self without first row and first column
        """
        S = []
        for row in self.m[1:]:
            S.append(row[1:])
        return matrix(S)

    def upperTriangular(self):
        """
        converts to upper triangular form
        """
        self.reduceColumn()
        if len(self.m) == 2:
            return self
        subMat = self.subMatrix().upperTriangular()
        for index in range(len(subMat.m)):
            self.m[index + 1] = ([0] + subMat.m[index])
        return self

    def utToDiag(self):
        """
        converts upper triangular to diagonal
        """
        if len(self.m) == 1:
            return self
        for index1 in range(len(self.m) - 1, 0, -1):
            for index2 in range(index1 - 1, -1, -1):
                if self.m[index2][index1] == 0 or self.m[index1][index1] == 0:
                    continue
                factor = ((self.m[index2][index1]) / (self.m[index1][index1] * 1.0))
                for column in range(len(self.m[index1])):
                    self.m[index2][column] = self.m[index2][column] - (self.m[index1][column] * factor)
        return  # Ta da!

    def normalize(self):
        """

        Returns:

        """
        for row in range(len(self.m)):
            factor = 1.0
            for column in self.m[row]:
                if column != 0:
                    factor = column
                    break
            for column in range(len(self.m[row])):
                self.m[row][column] = self.m[row][column] / (factor * 1.0)
        return

    def solve(self):
        """

        Returns:

        """
        self.upperTriangular()
        self.utToDiag()
        self.normalize()
        answer = []
        for index in range(len(self.m)):
            try:
                answer.append(self.m[index][-1] / self.m[index][index] * -1.0)
            except:
                answer.append(0)  # divided by 0.
        return answer

    def __repr__(self):
        return repr(self.m)


def line2dFromPoints(P1, P2):
    """
    Must be a cleaner way to do this? in line class?
    """
    x1, y1 = P1
    x2, y2 = P2
    if y1 != y2:
        M = matrix([[y1] + [-1] + [x1], [y2] + [-1] + [x2]])
        b, c = M.solve()
        return line2d(1, b, c)
    else:
        M = matrix([[x1] + [-1] + [y1], [x2] + [-1] + [y2]])
        a, c = M.solve()
        return line2d(a, 1, c)


class plane3d:
    """
     these ought to be immutable.
    A plane of the form Z = aX + bY + c.
    (We don't deal with sheer vertical planes.)
    """

    def __init__(self, P1, P2, P3):
        """
        init function takes 3 points in 3-space on the plane.
        This is surprisingly hard.
        We set up equations that look like
          A x1 + B y1 + C + (-z1) = 0
          A x2 + B y2 + C + (-z2) = 0
          A x3 + B y3 + C + (-z3) = 0
        and solve for A, B, and C.
        """
        M = matrix([[P1[0]] + [P1[1]] + [1] + [-1 * P1[2]], [P2[0]] + [P2[1]] + [1] + [-1 * P2[2]],
                    [P3[0]] + [P3[1]] + [1] + [-1 * P3[2]]])
        self.a, self.b, self.c = M.solve()
        return

    def __repr__(self):
        return "%fx + %fy + %f = z" % (self.a, self.b, self.c)

    def coeffs(self):
        """
        return coefficients a,b,c as a tuple
        """
        return self.a, self.b, self.c

    def value(self, P):
        """

        Args:
            P: 

        Returns:

        """
        return P[0] * self.a + P[1] * self.b + self.c
