# Registration website

The registration website is a Django application that allows users to register and participate in the VxRack Neutrino tutorial and play the Hero game. Once the users complete the registration form, this component will send a message to the Registration service that will be in charge of setting up the tutorial environment for the user and mailing him or her the credentials and instructions to get started with it.

Upon each completed registration, this components will generate a JSON message with the following fields.

| **Field** | **Required** | **Description** |
|---|---|---|
| `first_name` | yes | First name |
| `last_name` | yes | Last name |
| `email` | yes | Email address |
| `country` | yes | ISO 3166-1. Two-letter code of the country |
| `password` | yes | SHA256 of the password |
| `company` | no | Company name |
| `phone` | no | Phone number |
| `twitter_handle` | no | Twitter handle |
| `hero_name` | yes | Hero name |
| `hero_class` | yes | Hero class |
| `hero_title` | yes | Hero title |

Example:

```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "country": "ES",
    "password": "89e01536ac207279409d4de1e5253e01f4a1769e696db0d6062ca9b8f56767c8",
    "company": "EMC",
    "phone": "912312312",
    "twitter_handle": "john_doe",
    "hero_name": "Gandalf",
    "hero_class": "Magician",
    "hero_title": "The Great"
}
```

## Docker

You can build the production image with the provided `Dockerfile`.

```
docker build -t hero-web .
```

And run it with your connection details to RabbitMQ.

```
docker run -d \
  --env-file hero.env \
  --link rabbitmq  \
  -p 8000:8080 \
  --name hero-web \
  hero-web
```
