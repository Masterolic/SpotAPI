from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any, Sequence

from spotapi.client import BaseClient
from spotapi.http.request import TLSClient
from spotapi.types.annotations import enforce

__all__ = ["Search"]


@enforce
class Search:
    """
    Search Spotify using the same top-results query used by the Spotify
    web player.

    Parameters
    ----------
    client : TLSClient, optional
        A TLSClient used for making requests. A Chrome 120 client is used
        by default.
    """

    __slots__ = ("base",)

    def __init__(
        self,
        *,
        client: TLSClient = TLSClient("chrome_120", "", auto_retries=3),
    ) -> None:
        self.base = BaseClient(client=client)

    def query_search(
        self,
        query: str,
        /,
        limit: int = 50,
        *,
        offset: int = 0,
        number_of_top_results: int = 50,
        section_filters: Sequence[str] = ("GENERIC", "VIDEO_CONTENT"),
        include_album_pre_releases: bool = False,
        include_artist_has_concerts_field: bool = False,
        include_audiobooks: bool = True,
        include_authors: bool = True,
        include_episode_content_ratings_v2: bool = True,
        include_pre_releases: bool = True,
        is_prefix: bool | None = None,
    ) -> Mapping[str, Any]:
        """
        Searches Spotify using the web player's searchTopResultsList
        operation.

        The defaults mirror the request observed from Spotify Web:
        limit=50, numberOfTopResults=50 and the GENERIC /
        VIDEO_CONTENT sections.

        Returns
        -------
        Mapping[str, Any]
            The raw Spotify Pathfinder response.
        """
        if not query:
            raise ValueError("Search query cannot be empty")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if offset < 0:
            raise ValueError("offset cannot be negative")

        if number_of_top_results < 1:
            raise ValueError("number_of_top_results must be greater than 0")

        url = "https://api-partner.spotify.com/pathfinder/v1/query"

        variables = {
            "query": query,
            "limit": limit,
            "offset": offset,
            "numberOfTopResults": number_of_top_results,
            "includeAlbumPreReleases": include_album_pre_releases,
            "includeArtistHasConcertsField": include_artist_has_concerts_field,
            "includeAudiobooks": include_audiobooks,
            "includeAuthors": include_authors,
            "includeEpisodeContentRatingsV2": include_episode_content_ratings_v2,
            "includePreReleases": include_pre_releases,
            "isPrefix": is_prefix,
            "sectionFilters": list(section_filters),
        }

        params = {
            "operationName": "searchTopResultsList",
            "variables": json.dumps(variables, separators=(",", ":")),
            "extensions": json.dumps(
                {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "dd78eaff943eba629ed70ee25517b9cea0dcaa41193e2592ae2727660b21892c", #self.base.part_hash("searchTopResultsList"),
                    }
                },
                separators=(",", ":"),
            ),
        }

        resp = self.base.client.post(
            url,
            params=params,
            authenticate=True,
        )

        if resp.fail:
            raise RuntimeError(
                "Could not search Spotify",
                resp.error.string,
            )

        if not isinstance(resp.response, Mapping):
            raise RuntimeError("Invalid JSON response")

        return resp.response

    def search(
        self,
        query: str,
        /,
        limit: int = 50,
        *,
        offset: int = 0,
        number_of_top_results: int = 50,
        section_filters: Sequence[str] = ("GENERIC", "VIDEO_CONTENT"),
    ) -> Mapping[str, Any]:
        """Convenience alias for query_search."""
        return self.query_search(
            query,
            limit=limit,
            offset=offset,
            number_of_top_results=number_of_top_results,
            section_filters=section_filters,
        )
