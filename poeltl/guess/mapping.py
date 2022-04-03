from .context import BinaryAttributeContext, GameContext, VariableCloseAttributeContext, VariableAttributeContext
from .feedback import AttributeFeedback, AttributeStatus, GuessFeedback


def map_feedback_to_context(guess_feedback: GuessFeedback, game_context: GameContext) -> GameContext:
    _map_attribute_feedback_to_variable_attribute_context(guess_feedback.team_code_feedback, game_context.team_code_context)
    _map_attribute_feedback_to_binary_attribute_context(guess_feedback.conference_name_feedback, game_context.conference_name_context)
    _map_attribute_feedback_to_variable_attribute_context(guess_feedback.division_abbreviation_feedback, game_context.division_abbreviation_context)
    _map_attribute_feedback_to_variable_close_attribute_context(guess_feedback.player_position_feedback, game_context.player_position_context)
    _map_attribute_feedback_to_variable_close_attribute_context(guess_feedback.player_height_inches_feedback, game_context.player_height_inches_context)
    _map_attribute_feedback_to_variable_close_attribute_context(guess_feedback.player_age_feedback, game_context.player_age_context)
    _map_attribute_feedback_to_variable_close_attribute_context(guess_feedback.player_jersey_number_feedback, game_context.player_jersey_number_context)
    return game_context


def _map_attribute_feedback_to_binary_attribute_context(feedback: AttributeFeedback, context: BinaryAttributeContext):    
    if feedback.status == AttributeStatus.CORRECT:
        context.correct_value = feedback.value
    elif feedback.status == AttributeStatus.INCORRECT:
        context.incorrect_value = feedback.value
    else:
        raise ValueError(f"Unsupported attribute feedback status '{feedback.status}' for binary attribute")    


def _map_attribute_feedback_to_variable_attribute_context(feedback: AttributeFeedback, context: VariableAttributeContext):    
    if feedback.status == AttributeStatus.CORRECT:
        context.correct_value = feedback.value
    elif feedback.status == AttributeStatus.INCORRECT:
        context.incorrect_values.append(feedback.value)
    else:
        raise ValueError(f"Unsupported attribute feedback status '{feedback.status}' for variable attribute")    


def _map_attribute_feedback_to_variable_close_attribute_context(feedback: AttributeFeedback, context: VariableCloseAttributeContext):
    if feedback.status == AttributeStatus.CORRECT:
        context.correct_value = feedback.value
    elif feedback.status == AttributeStatus.INCORRECT:
        context.incorrect_values.append(feedback.value)
    elif feedback.status == AttributeStatus.CLOSE:
        context.close_values.append(feedback.value)
    else:
        raise ValueError(f"Unsupported attribute feedback status '{feedback.status}' for variable close attribute")
