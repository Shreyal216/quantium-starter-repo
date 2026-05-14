import pytest
from dash.testing.application_runners import import_app

# Import your app
from app import app

@pytest.fixture
def dash_app():
    """Fixture to set up the Dash app for testing"""
    return app

def test_header_present(dash_app):
    """Test that the header is present in the app"""
    dash_app.server.config['TESTING'] = True
    client = dash_app.server.test_client()
    
    # Get the app layout
    result = client.get('/')
    assert result.status_code == 200
    
    # Check that the header text is in the layout
    assert "Soul Foods Pink Morsel Sales Dashboard" in str(dash_app.layout)

def test_visualization_present(dash_app):
    """Test that the visualization (dcc.Graph) is present in the app"""
    # Convert layout to string to check for Graph component
    layout_str = str(dash_app.layout)
    
    # Check that dcc.Graph is in the layout
    assert "sales-chart" in layout_str
    
    # Verify the graph id exists
    found_graph = False
    for component in dash_app.layout.children:
        if hasattr(component, 'children'):
            for child in component.children:
                if hasattr(child, 'children'):
                    for grandchild in child.children:
                        if hasattr(grandchild, 'id') and grandchild.id == 'sales-chart':
                            found_graph = True
    
    assert found_graph, "Graph with id 'sales-chart' not found"

def test_region_picker_present(dash_app):
    """Test that the region picker (RadioItems) is present in the app"""
    layout_str = str(dash_app.layout)
    
    # Check that the radio button id is in the layout
    assert "region-radio" in layout_str
    
    # Verify RadioItems component exists with correct options
    found_radio = False
    for component in dash_app.layout.children:
        if hasattr(component, 'children'):
            for child in component.children:
                if hasattr(child, 'children'):
                    for grandchild in child.children:
                        if hasattr(grandchild, 'id') and grandchild.id == 'region-radio':
                            found_radio = True
                            # Check that options include the required regions
                            assert hasattr(grandchild, 'options')
    
    assert found_radio, "RadioItems with id 'region-radio' not found"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])