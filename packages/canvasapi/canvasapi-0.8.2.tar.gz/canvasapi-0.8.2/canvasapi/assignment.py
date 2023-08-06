from __future__ import absolute_import, division, print_function, unicode_literals

from six import python_2_unicode_compatible

from canvasapi.canvas_object import CanvasObject
from canvasapi.util import combine_kwargs


@python_2_unicode_compatible
class Assignment(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def delete(self):
        """
        Delete this assignment.

        :calls: `DELETE /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments.destroy>`_

        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        response = self._requester.request(
            'DELETE',
            'courses/{}/assignments/{}'.format(self.course_id, self.id),
        )
        return Assignment(self._requester, response.json())

    def edit(self, **kwargs):
        """
        Modify this assignment.

        :calls: `PUT /api/v1/courses/:course_id/assignments/:id \
        <https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update>`_

        :rtype: :class:`canvasapi.assignment.Assignment`
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/assignments/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(Assignment, self).set_attributes(response.json())

        return Assignment(self._requester, response.json())


@python_2_unicode_compatible
class AssignmentGroup(CanvasObject):

    def __str__(self):
        return "{} ({})".format(self.name, self.id)

    def edit(self, **kwargs):
        """
        Modify this assignment group.

        :calls: `PUT /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.update>`_

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        response = self._requester.request(
            'PUT',
            'courses/{}/assignment_groups/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )

        if 'name' in response.json():
            super(AssignmentGroup, self).set_attributes(response.json())

        return AssignmentGroup(self._requester, response.json())

    def delete(self, **kwargs):
        """
        Delete this assignment.

        :calls: `DELETE /api/v1/courses/:course_id/assignment_groups/:assignment_group_id \
        <https://canvas.instructure.com/doc/api/assignment_groups.html#method.assignment_groups_api.destroy>`_

        :rtype: :class:`canvasapi.assignment.AssignmentGroup`
        """
        response = self._requester.request(
            'DELETE',
            'courses/{}/assignment_groups/{}'.format(self.course_id, self.id),
            _kwargs=combine_kwargs(**kwargs)
        )
        return AssignmentGroup(self._requester, response.json())
