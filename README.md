## LILIT's astrological API servrice

<br>

> a python-based api service for performing astrological calculations.

<br>

---

### local development

<br>

create a virtual environment and install depedencies:

```bash
make install
source venv/bin/activate
```

<br>

to start the server (on [localhost:8000](http://localhost:8000)):

```bash
make server
```

<br>

or, using docker:

```bash
make server-dev
make server-dev-stop
```

<br>

interactive api documentation: [localhost:8000/docs](http://localhost:8000/docs).

<br>

---

### API authentication

<br>

> this service requires an API key for all endpoints except the documentation. 

<br>

to generate a new API key:

```bash
make key
```

<br>

you can then add this key to `.env`. To support multiple API keys, add them as a comma-separated list in the `API_KEYS` environment variable:

```bash
API_KEYS=key1,key2,key3
```

<br>

#### security features

<br>

the API includes several security features:

- rate limiting (requests per hour per IP)
- failed attempt tracking (IPs are temporarily blocked after a number of failed attempts)
- CORS protection (only allows requests from specified origins)
- secure headers: (inly allows necessary HTTP methods and headers)

<br>

to configure allowed origins for CORS, set the `ALLOWED_ORIGINS` environment variable:

```bash
ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
```

<br>

---

### endpoints

<br>

#### `docs/`

<br>

```bash
curl "http://localhost:8000/docs"
```    

<br>

#### `planets/`

<br>

```bash
curl "http://localhost:8000/planets?API_KEY=<your-api>"
```    

<br>

---

### prod setup

<br>

run:

```bash
make server-prod
```

<br>

stop the service:

```bash
make kill
```

<br>

view logs:

```bash
make logs
```
