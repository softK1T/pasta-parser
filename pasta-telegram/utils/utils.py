from datetime import datetime, timezone
import re

from config import config

positive_reactions = ['👍', '❤', '🔥']
neutral_reactions = ['🤔']
negative_reactions = ['👎']


def format_date(date):
    """Formats the Telethon datetime to UTC datetime with timezone info."""
    return datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, tzinfo=timezone.utc)


def extract_url(message):
    """Extracts URL from the message text using regular expression."""
    if message.message is None:
        return None
    return re.search(r"http[s]?://[^\s]+", message.message)


def group_reactions(reactions):
    """Groups the reactions into positive, neutral, and negative categories."""
    positive = 0
    neutral = 0
    negative = 0
    for reaction in reactions:
        if reaction.reaction.emoticon in positive_reactions:
            positive += reaction.count
        elif reaction.reaction.emoticon in neutral_reactions:
            neutral += reaction.count
        elif reaction.reaction.emoticon in negative_reactions:
            negative += reaction.count

    sum = positive + neutral + negative
    ratio = (positive / sum * 100).__round__(2) if sum != 0 else -1
    return [positive, neutral, negative, sum, ratio]


def transform_msg(message, url, reactions):
    """Transforms a Telegram message to a dictionary for MongoDB storage."""
    if url is None:
        return None
    try:
        return {
            '_id': message.id,  # Use message ID as unique identifier
            'pasta_url': url.group(),
            'timestamp': format_date(message.date),
            'positive_reactions': reactions[0],
            'neutral_reactions': reactions[1],
            'negative_reactions': reactions[2],
            'overall_reactions': reactions[3],
            'ratio': reactions[4],
            'message_url': f'https://t.me/{config.CHANNEL_USERNAME}/{message.id}',
            'updated_at': format_date(datetime.now())
        }
    except AttributeError:
        return None


def format_messages(messages):
    """Formats a list of Telegram messages, extracting and transforming valid URLs."""
    formatted = []
    for message in messages:
        url_match = extract_url(message)
        if url_match:
            if hasattr(message, 'reactions') and message.reactions is not None:
                reactions = group_reactions(message.reactions.results)
            else:
                reactions = [0, 0, 0, 0, -1]  # Default values if no reactions are present or reactions is None
            formatted_msg = transform_msg(message, url_match, reactions)
            if formatted_msg:
                formatted.append(formatted_msg)
    return formatted
