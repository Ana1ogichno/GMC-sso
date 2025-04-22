from app.config.contracts import IErrorTableFormatter, IAppDescriptionBuilder


class AppDescriptionBuilder(IAppDescriptionBuilder):
    """
    Builds the full app description with collapsible error code section.
    """

    def __init__(
        self,
        errors_formatter: IErrorTableFormatter,
    ):
        """
        Initialize the formatter with a centralized error enumeration container.

        :param errors_formatter: An implementation of IErrorCodesEnums that contains grouped error enums.
        """

        self._errors = errors_formatter

    def build_description(self) -> str:
        return f"""
<details>
<summary>Коды возможных ошибок сервиса</summary>
<br>

| Код ошибки | Имя ошибки                | Описание       |
|------------|---------------------------|----------------|
{self._errors.generate_table()}
</details>
"""
