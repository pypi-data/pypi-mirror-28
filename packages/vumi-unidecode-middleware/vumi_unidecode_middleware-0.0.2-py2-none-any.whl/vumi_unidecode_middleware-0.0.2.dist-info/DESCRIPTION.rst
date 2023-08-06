# vumi-unidecode-middleware
[Vumi][vumi] middleware that runs message content through unidecode

## Using the middleware

The path to the middleware class is
`vumi_unidecode_middleware.UnidecodeMiddleware`.

There are two optional config parameters.

`message_direction` must be one of `inbound`, `outbound`, or `both`. This
limits whether to transform inbound, outbound, or both inbound and outbound
messages. Defaults to `both`

`ignore_characters` is a string of characters that, excluding ASCII characters,
will be excluded from being converted. Defaults to no characters.

For more information on how to run vumi middleware, please consult the [vumi
middleware documentation][vumi_middleware].

## Testing

To run the tests, install the dependancies and use the trial test runner:

    pip install -e .
    trial vumi_unidecode_middleware


[vumi]: https://github.com/praekelt/vumi
[vumi_middleware]: https://vumi.readthedocs.io/en/latest/middleware/index.html


