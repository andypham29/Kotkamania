# [NHLMockDraft](https://nhlmockdraft2020.herokuapp.com/)
deployed on [Render](https://dashboard.render.com/)
## Installation $ Setup
`$ pip install virtualenv`

`$ python -m virtualenv venv`

### Install requirements
`$ pip install -r requirements.txt`

`$ cd venv/Scripts/`

`$ .\activate`

`$ pip freeze > requirements.txt (cd to root of project)`

### Run the app

`$ python app.py`

## API
/api/prospects	

	?id={id}
	
	?page={page} 		// page can be combined with below search criteria
	
	?position={position}
	
	?league{league}

/api/drafts

	?ranked={isRanked}
