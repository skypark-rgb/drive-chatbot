Current status
- App runs locally in Streamlit.
- Uses Google Drive API service account.
- Uses OpenAI API.
- Uses local Qdrant and SQLite.

Needed for company-wide testing
- Shared Drive/folder must be shared with service account as Viewer (read-only access).
    - Emailed Laurence✅
- Service account currently: drive-chatbot@drivechatbot-499722.iam.gserviceaccount.com

Near-term deployment path
1. Test on company-wide shared folder locally.
2. Move secrets out of local files.
3. Deploy Streamlit app.
4. Move Qdrant from local embedded mode to server/cloud mode if needed.
5. Add authentication or team-specific chatbot access later.


Required for online testing:
- GitHub repo up to date.
- requirements.txt complete.
- API keys moved to Streamlit secrets.
- Service account shared with target Drive folder as Viewer.
- Decide whether Qdrant Local is acceptable for demo or move to Qdrant server/cloud.


Authorization plan:
- Prototype: manual allowlist.
- Next: Google login / organization email verification.
- Later: team-specific access by chatbot/folder.


Risks
- Qdrant Local is not ideal for production use.
- Python dependencies should be pinned.
- Service account ownership should be transferred or confirmed before production.