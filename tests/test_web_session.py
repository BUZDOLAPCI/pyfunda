import unittest

from funda import Funda
from funda.constants import WEB_SEARCH_IMPERSONATE


class WebSessionImpersonateTests(unittest.TestCase):
    def test_default_tracks_curl_cffi_newest_chrome(self) -> None:
        """The default must not pin an ageing release.

        Akamai stops accepting Chrome fingerprints once they age out, which made the
        web-search fallback fail with `curl (92) ... INTERNAL_ERROR`. Deferring to
        curl_cffi's own alias means a curl_cffi upgrade is enough to recover.
        """
        self.assertEqual(WEB_SEARCH_IMPERSONATE, "chrome")
        self.assertEqual(Funda().web_impersonate, "chrome")

    def test_session_uses_configured_target(self) -> None:
        client = Funda(web_impersonate="chrome131")
        try:
            self.assertIs(client.web_session, client.web_session)  # cached
            self.assertEqual(client.web_impersonate, "chrome131")
        finally:
            client.close()

    def test_alias_resolves_to_a_concrete_recent_target(self) -> None:
        from curl_cffi.requests.impersonate import DEFAULT_CHROME

        self.assertTrue(DEFAULT_CHROME.startswith("chrome"))
        # Chrome 124 dates from April 2024 and is the version Akamai now rejects.
        self.assertNotEqual(DEFAULT_CHROME, "chrome124")

    def test_dutch_accept_language_is_preserved(self) -> None:
        client = Funda()
        try:
            self.assertIn("nl-NL", client.web_session.headers["accept-language"])
        finally:
            client.close()


if __name__ == "__main__":
    unittest.main()
