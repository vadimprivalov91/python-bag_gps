from rest_framework.negotiation import DefaultContentNegotiation


class MyContentNegotiation(DefaultContentNegotiation):
    def select_parser(self, request, parsers):
        return super().select_parser(request, parsers)

    def select_renderer(self, request, renderers, format_suffix):
        return super().select_renderer(request, renderers, format_suffix)
