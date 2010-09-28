from abjad import *


def test_containertools_delete_contents_of_container_starting_strictly_before_prolated_offset_01( ):
   
   staff = Staff(macros.scale(4))
   spannertools.BeamSpanner(staff.leaves)
   containertools.delete_contents_of_container_starting_strictly_before_prolated_offset(staff, Fraction(1, 8))

   r'''
   \new Staff {
        d'8 [
        e'8
        f'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == "\\new Staff {\n\td'8 [\n\te'8\n\tf'8 ]\n}"


def test_containertools_delete_contents_of_container_starting_strictly_before_prolated_offset_02( ):

   staff = Staff(macros.scale(4))
   spannertools.BeamSpanner(staff.leaves)
   containertools.delete_contents_of_container_starting_strictly_before_prolated_offset(staff, Fraction(3, 16))

   r'''
   \new Staff {
        e'8 [
        f'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == "\\new Staff {\n\te'8 [\n\tf'8 ]\n}"


def test_containertools_delete_contents_of_container_starting_strictly_before_prolated_offset_03( ):
   '''Delete nothing when no contents start before prolated offset.'''

   staff = Staff(macros.scale(4))
   spannertools.BeamSpanner(staff.leaves)
   containertools.delete_contents_of_container_starting_strictly_before_prolated_offset(staff, 0)

   r'''
   \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == "\\new Staff {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_containertools_delete_contents_of_container_starting_strictly_before_prolated_offset_04( ):
   '''Delete all contents when all elements start before prolated offset.'''

   staff = Staff(macros.scale(4))
   spannertools.BeamSpanner(staff.leaves)
   containertools.delete_contents_of_container_starting_strictly_before_prolated_offset(staff, 99)

   r'''
   \new Staff {
   }
   '''

   assert componenttools.is_well_formed_component(staff)
   assert staff.format == '\\new Staff {\n}'
