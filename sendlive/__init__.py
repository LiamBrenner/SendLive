"""Main sendlive package."""
from typing import Optional
from pydantic import BaseModel, computed_field

from sendlive.constants import ProviderOptions, ServiceProvider
from sendlive.stream import BaseStream
from sendlive.utils import get_adapter_for_provider
from sendlive.constants import (
    BaseCredential,
    ServiceProvider,
)
from sendlive.adapter import BaseAdapter


class SendLive(BaseModel):
    """SendLive is a library for creating live streams with different cloud vendors, using one interface."""

    credentials: BaseCredential
    provider_options: Optional[ProviderOptions] = None

    @property
    def service_provider(self) -> ServiceProvider:
        """Return the service provider, based on the provided credentials."""
        return self.credentials.service_provider

    @computed_field
    @property
    def adapter(self) -> BaseAdapter:
        """Return the adapter for the configured service provider."""
        adapter_cls = get_adapter_for_provider(provider=self.service_provider)
        return adapter_cls(
            credentials=self.credentials, provider_options=self.provider_options
        )

    def create_stream(
        self,
        name: str,
    ) -> BaseStream:
        """Create a stream using the configured service provider."""
        return self.adapter.create_stream(name=name)
