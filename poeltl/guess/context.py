class AttributeContext:
    
    def __init__(self, correct_value=None):
        self._correct_value = correct_value

    @property
    def correct_value(self):
        return self._correct_value

    @correct_value.setter
    def correct_value(self, value):
        self._correct_value = value


class BinaryAttributeContext(AttributeContext):

    def __init__(self, correct_value=None, incorrect_value=None):
        super().__init__(correct_value)
        self._incorrect_value = incorrect_value

    @property
    def incorrect_value(self):
        return self._incorrect_value

    @incorrect_value.setter
    def incorrect_value(self, value):
        self._incorrect_value = value


class VariableAttributeContext(AttributeContext):

    def __init__(self, correct_value=None, incorrect_values=None):
        super().__init__(correct_value)
        if incorrect_values is None:
            self._incorrect_values = []
        else:
            self._incorrect_values = incorrect_values

    @property
    def incorrect_values(self):
        return self._incorrect_values

    @incorrect_values.setter
    def incorrect_values(self, values):
        self._incorrect_values = values


class VariableCloseAttributeContext(VariableAttributeContext):
    
    def __init__(self, correct_value=None, incorrect_values=None, close_values=None):
        super().__init__(correct_value, incorrect_values)
        if close_values is None:
            self._close_values = []
        else:
            self._close_values = close_values

    @property
    def close_values(self):
        return self._close_values

    @close_values.setter
    def close_values(self, values):
        self._close_values = values


"""
Flavors of AttributeContext by example:

Team.code --> VariableAttributeContext
  CORRECT:    'MIN' (e.g.) or None
  INCORRECT:  ['LAL', 'OKC', ...] or []
  CLOSE:      n/a

Conference.name --> BinaryAttributeContext
  CORRECT:    'East' (e.g.) or None
  INCORRECT:  'East' (e.g.) or None
  CLOSE:      n/a

Division.abbreviation --> VariableAttributeContext
  CORRECT:    'NW' (e.g.) or None
  INCORRECT:  ['Pac.', 'SW', ...] or []
  CLOSE:      n/a

NOTE: For VariableCloseAttributeContext, CLOSE is a subset of INCORRECT

Player.position --> VariableCloseAttributeContext
  CORRECT:    'C' (e.g.) or None
  INCORRECT:  ['G', 'G-F', ...] or []
  CLOSE:      ['G-F', ...] or []

Player.height_inches --> VariableCloseAttributeContext
  CORRECT:    79 or None
  INCORRECT:  [74/low, 78/low, 81/high, 85/high, ...] or []
  CLOSE:      [78/low, 81/high, ...] or []

Player.birth_date (age) --> VariableCloseAttributeContext
  CORRECT:    26 or None
  INCORRECT:  [22/low, 24/low, 27/high, 30/high, ...] or []
  CLOSE:      [24/low, 27/high, ...] or []

Player.jersey_number --> VariableCloseAttributeContext
  CORRECT:    32 or None
  INCORRECT:  [2/low, 30/low, 33/high, 45/high, ...] or []
  CLOSE:      [30/low, 33/high, ...] or []
"""
