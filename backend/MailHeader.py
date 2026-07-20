from typing import TypedDict

GmailHeader = TypedDict('GmailHeader', {
    "id": str,
    "threadId": str,
    "labelIds": str,
    "snippet": str,
    "internalDate": str,
    "delivered-To": str,
    "return-Path": str,
    "date": str, 
    "subject": str, 
    "from": str,
    "to": str, 
    "sender": str, 
    "reply-to": str,
    "mimeType": str,
    "formattedDate": str
  }
)

emailIdTime = TypedDict('emailIdTime', {
    "id": str,
    "threadId": str,
    "internalDate": str,
  }
)

  