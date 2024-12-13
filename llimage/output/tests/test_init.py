"""
Tests for output module initialization and formatter creation.
"""

import pytest
from llimage.output import (
    create_formatter,
    JsonFormatter,
    TextFormatter,
    DEFAULT_CONFIG
)

def test_create_json_formatter():
    """Test creation of JSON formatter."""
    formatter = create_formatter('json')
    assert isinstance(formatter, JsonFormatter)
    assert formatter.detail_level == DEFAULT_CONFIG['detail_level']
    assert formatter.include_metadata == DEFAULT_CONFIG['include_metadata']
    assert formatter.pretty_print == DEFAULT_CONFIG['pretty_print']

def test_create_text_formatter():
    """Test creation of text formatter."""
    formatter = create_formatter('text')
    assert isinstance(formatter, TextFormatter)
    assert formatter.detail_level == DEFAULT_CONFIG['detail_level']
    assert formatter.include_metadata == DEFAULT_CONFIG['include_metadata']

def test_create_formatter_with_config():
    """Test formatter creation with custom configuration."""
    config = {
        'detail_level': 'detailed',
        'include_metadata': False,
        'pretty_print': False
    }
    
    # Test JSON formatter
    json_formatter = create_formatter('json', config)
    assert json_formatter.detail_level == 'detailed'
    assert json_formatter.include_metadata is False
    assert json_formatter.pretty_print is False
    
    # Test text formatter
    text_formatter = create_formatter('text', config)
    assert text_formatter.detail_level == 'detailed'
    assert text_formatter.include_metadata is False

def test_create_formatter_case_insensitive():
    """Test that formatter creation is case insensitive."""
    assert isinstance(create_formatter('JSON'), JsonFormatter)
    assert isinstance(create_formatter('Text'), TextFormatter)
    assert isinstance(create_formatter('json'), JsonFormatter)
    assert isinstance(create_formatter('text'), TextFormatter)

def test_create_formatter_invalid_type():
    """Test error handling for invalid formatter type."""
    with pytest.raises(ValueError) as exc_info:
        create_formatter('invalid')
    assert "Invalid format type" in str(exc_info.value)

def test_default_config_values():
    """Test that DEFAULT_CONFIG has expected values."""
    assert 'detail_level' in DEFAULT_CONFIG
    assert 'include_metadata' in DEFAULT_CONFIG
    assert 'include_confidence' in DEFAULT_CONFIG
    assert 'pretty_print' in DEFAULT_CONFIG
    
    assert DEFAULT_CONFIG['detail_level'] == 'standard'
    assert DEFAULT_CONFIG['include_metadata'] is True
    assert DEFAULT_CONFIG['include_confidence'] is True
    assert DEFAULT_CONFIG['pretty_print'] is True

def test_module_exports():
    """Test that __all__ exports expected names."""
    import llimage.output
    
    assert hasattr(llimage.output, 'JsonFormatter')
    assert hasattr(llimage.output, 'TextFormatter')
    assert hasattr(llimage.output, 'create_formatter')
    
    # Test that exported names match __all__
    for name in llimage.output.__all__:
        assert hasattr(llimage.output, name)
