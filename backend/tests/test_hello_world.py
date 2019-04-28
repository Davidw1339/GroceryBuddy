def test_hello_world(client):
    '''
    Tests that the hello world test route is responsive.
    '''
    rv = client.get('/')
    assert rv.data.decode('ascii') == 'Hello, Grocery buddies!'
