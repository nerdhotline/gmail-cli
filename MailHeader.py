from typing import TypedDict

GmailHeader = TypedDict('GmailHeader', {
    "id": str,
    "threadId": str,
    "labelIds": str,
    "snippet": str,
    "internalDate": str,
    "Delivered-To": str,
    "Return-Path": str,
    "Date": str, 
    "Subject": str, 
    "From": str,
    "To": str, 
    "Sender": str, 
    "Reply-To": str,
    "mimeType": str,
    "formattedDate": str
  }
)

  