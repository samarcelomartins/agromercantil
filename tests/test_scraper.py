import unittest
from unittest.mock import patch, Mock
import requests
import hashlib
from scraper import get_page_content, calculate_hash, detect_layout_changes

class TestScraper(unittest.TestCase):
    
    @patch('scraper.requests.get')
    def test_get_page_content(self, mock_get):
        # Configura o mock para simular a resposta do requests.get
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'Fake page content'
        mock_get.return_value = mock_response
        
        url = 'https://example.com/produtos'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        
        content = get_page_content(url, headers)
        self.assertEqual(content, 'Fake page content')
    
    def test_calculate_hash(self):
        content = 'Fake page content'
        expected_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        self.assertEqual(calculate_hash(content), expected_hash)
    
    @patch('scraper.get_page_content')
    def test_detect_layout_changes(self, mock_get_page_content):
        mock_get_page_content.side_effect = [
            'Fake page content', 
            'Changed page content'
        ]
        
        url = 'https://example.com/produtos'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        
        # Primeira chamada sem hash anterior
        change_detected, previous_hash = detect_layout_changes(url, headers)
        self.assertFalse(change_detected)
        
        # Segunda chamada com hash anterior
        change_detected, new_hash = detect_layout_changes(url, headers, previous_hash)
        self.assertTrue(change_detected)
        self.assertNotEqual(previous_hash, new_hash)

if __name__ == '__main__':
    unittest.main()
