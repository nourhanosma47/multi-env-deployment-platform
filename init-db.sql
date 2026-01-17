-- Create items table
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO items (name, description) VALUES
    ('Laptop', 'High performance laptop for development'),
    ('Monitor', '27 inch 4K monitor'),
    ('Keyboard', 'Mechanical keyboard with RGB');

-- Create index for better performance
CREATE INDEX idx_items_created_at ON items(created_at DESC);
