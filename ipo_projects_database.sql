-- IPO Management System Database Schema and Sample Data
-- Database: ipos_db
-- Created for Django IPO Management System

-- Create Database
CREATE DATABASE ipos_db;
\c ipos_db;

-- Create User (if needed)
-- CREATE USER ipo_user WITH PASSWORD 'your_password';
-- GRANT ALL PRIVILEGES ON DATABASE ipos_db TO ipo_user;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- DJANGO AUTH TABLES (Required for Django Admin)
-- =====================================================

-- Django auth_user table
CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Django auth_group table
CREATE TABLE auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) UNIQUE NOT NULL
);

-- Django auth_permission table
CREATE TABLE auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL
);

-- Django content_type table
CREATE TABLE django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
);

-- Django session table
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Django admin log table
CREATE TABLE django_admin_log (
    id SERIAL PRIMARY KEY,
    action_time TIMESTAMP WITH TIME ZONE NOT NULL,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL,
    change_message TEXT NOT NULL,
    content_type_id INTEGER,
    user_id INTEGER NOT NULL
);

-- =====================================================
-- IPO MANAGEMENT SYSTEM TABLES
-- =====================================================

-- Company table
CREATE TABLE ipo_company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) UNIQUE NOT NULL,
    logo VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- IPO table
CREATE TABLE ipo_ipo (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES ipo_company(id) ON DELETE CASCADE,
    price_band_lower NUMERIC(10,2) NOT NULL,
    price_band_upper NUMERIC(10,2) NOT NULL,
    open_date DATE NOT NULL,
    close_date DATE NOT NULL,
    issue_size NUMERIC(15,2) NOT NULL,
    issue_type VARCHAR(20) NOT NULL DEFAULT 'book_building',
    listing_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'upcoming',
    ipo_price NUMERIC(10,2),
    listing_price NUMERIC(10,2),
    current_market_price NUMERIC(10,2),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT ipo_status_check CHECK (status IN ('upcoming', 'ongoing', 'listed')),
    CONSTRAINT ipo_issue_type_check CHECK (issue_type IN ('book_building', 'fixed_price', 'auction'))
);

-- Document table
CREATE TABLE ipo_document (
    id SERIAL PRIMARY KEY,
    ipo_id INTEGER NOT NULL REFERENCES ipo_ipo(id) ON DELETE CASCADE,
    rhp_pdf VARCHAR(100),
    drhp_pdf VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- FAQ table
CREATE TABLE ipo_faq (
    id SERIAL PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    answer TEXT NOT NULL,
    "order" INTEGER NOT NULL DEFAULT 0,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Company indexes
CREATE INDEX idx_company_name ON ipo_company(name);
CREATE INDEX idx_company_created_at ON ipo_company(created_at);

-- IPO indexes
CREATE INDEX idx_ipo_company_id ON ipo_ipo(company_id);
CREATE INDEX idx_ipo_status ON ipo_ipo(status);
CREATE INDEX idx_ipo_open_date ON ipo_ipo(open_date);
CREATE INDEX idx_ipo_listing_date ON ipo_ipo(listing_date);
CREATE INDEX idx_ipo_issue_type ON ipo_ipo(issue_type);

-- Document indexes
CREATE INDEX idx_document_ipo_id ON ipo_document(ipo_id);

-- FAQ indexes
CREATE INDEX idx_faq_order ON ipo_faq("order");
CREATE INDEX idx_faq_active ON ipo_faq(active);

-- =====================================================
-- SAMPLE DATA
-- =====================================================

-- Insert sample companies
INSERT INTO ipo_company (name, logo, created_at, updated_at) VALUES
('Tata Technologies Limited', 'company_logos/tata_tech.png', NOW(), NOW()),
('IREDA Limited', 'company_logos/ireda.png', NOW(), NOW()),
('Mamaearth Parent Company', 'company_logos/mamaearth.png', NOW(), NOW()),
('JSW Infrastructure Limited', 'company_logos/jsw_infra.png', NOW(), NOW()),
('Cello World Limited', 'company_logos/cello_world.png', NOW(), NOW()),
('ASMAI Limited', 'company_logos/asmai.png', NOW(), NOW()),
('Protean eGov Technologies Limited', 'company_logos/protean.png', NOW(), NOW()),
('ESAF Small Finance Bank Limited', 'company_logos/esaf_bank.png', NOW(), NOW()),
('Rockingdeals Circular Economy Limited', 'company_logos/rockingdeals.png', NOW(), NOW()),
('Innova Captab Limited', 'company_logos/innova_captab.png', NOW(), NOW());

-- Insert sample IPOs
INSERT INTO ipo_ipo (company_id, price_band_lower, price_band_upper, open_date, close_date, issue_size, issue_type, listing_date, status, ipo_price, listing_price, current_market_price, created_at, updated_at) VALUES
-- Upcoming IPOs
(1, 475.00, 500.00, '2024-01-15', '2024-01-18', 3042.51, 'book_building', NULL, 'upcoming', NULL, NULL, NULL, NOW(), NOW()),
(2, 30.00, 32.00, '2024-01-22', '2024-01-25', 2150.21, 'book_building', NULL, 'upcoming', NULL, NULL, NULL, NOW(), NOW()),
(3, 308.00, 324.00, '2024-01-29', '2024-02-01', 1701.44, 'book_building', NULL, 'upcoming', NULL, NULL, NULL, NOW(), NOW()),

-- Ongoing IPOs
(4, 113.00, 119.00, '2024-01-08', '2024-01-11', 2800.00, 'book_building', NULL, 'ongoing', NULL, NULL, NULL, NOW(), NOW()),
(5, 617.00, 648.00, '2024-01-05', '2024-01-08', 1900.00, 'book_building', NULL, 'ongoing', NULL, NULL, NULL, NOW(), NOW()),

-- Listed IPOs
(6, 65.00, 68.00, '2023-12-18', '2023-12-21', 500.00, 'book_building', '2023-12-28', 'listed', 66.50, 72.00, 78.50, NOW(), NOW()),
(7, 792.00, 831.00, '2023-12-11', '2023-12-14', 490.00, 'book_building', '2023-12-21', 'listed', 811.50, 850.00, 920.00, NOW(), NOW()),
(8, 57.00, 60.00, '2023-12-04', '2023-12-07', 463.00, 'book_building', '2023-12-14', 'listed', 58.50, 62.00, 65.00, NOW(), NOW()),
(9, 60.00, 63.00, '2023-11-27', '2023-11-30', 300.00, 'book_building', '2023-12-07', 'listed', 61.50, 58.00, 55.00, NOW(), NOW()),
(10, 426.00, 448.00, '2023-11-20', '2023-11-23', 1440.00, 'book_building', '2023-11-30', 'listed', 437.00, 460.00, 485.00, NOW(), NOW());

-- Insert sample documents
INSERT INTO ipo_document (ipo_id, rhp_pdf, drhp_pdf, created_at, updated_at) VALUES
(1, 'ipo_documents/rhp/tata_tech_rhp.pdf', 'ipo_documents/drhp/tata_tech_drhp.pdf', NOW(), NOW()),
(2, 'ipo_documents/rhp/ireda_rhp.pdf', 'ipo_documents/drhp/ireda_drhp.pdf', NOW(), NOW()),
(3, 'ipo_documents/rhp/mamaearth_rhp.pdf', 'ipo_documents/drhp/mamaearth_drhp.pdf', NOW(), NOW()),
(4, 'ipo_documents/rhp/jsw_infra_rhp.pdf', 'ipo_documents/drhp/jsw_infra_drhp.pdf', NOW(), NOW()),
(5, 'ipo_documents/rhp/cello_world_rhp.pdf', 'ipo_documents/drhp/cello_world_drhp.pdf', NOW(), NOW());

-- Insert sample FAQs
INSERT INTO ipo_faq (question, answer, "order", active, created_at, updated_at) VALUES
('What is an IPO?', 'An Initial Public Offering (IPO) is the process through which a private company becomes publicly traded by offering its shares to the public for the first time.', 1, TRUE, NOW(), NOW()),
('How can I apply for an IPO?', 'You can apply for an IPO through your bank account, demat account, or using UPI. Most banks and brokers provide online IPO application facilities.', 2, TRUE, NOW(), NOW()),
('What is the difference between RHP and DRHP?', 'DRHP (Draft Red Herring Prospectus) is the initial draft document, while RHP (Red Herring Prospectus) is the final document filed with SEBI after incorporating all changes.', 3, TRUE, NOW(), NOW()),
('What is the price band in an IPO?', 'The price band is the range within which investors can bid for shares. The upper and lower limits are set by the company and merchant bankers.', 4, TRUE, NOW(), NOW()),
('How is the listing gain calculated?', 'Listing gain is calculated as the percentage increase from the IPO price to the listing price: ((Listing Price - IPO Price) / IPO Price) × 100.', 5, TRUE, NOW(), NOW()),
('What documents are required for IPO application?', 'You need a PAN card, demat account, and bank account. Some IPOs may require additional KYC documents.', 6, TRUE, NOW(), NOW()),
('Can I apply for multiple lots in an IPO?', 'Yes, you can apply for multiple lots, but the total application amount should not exceed the maximum limit set by SEBI (usually Rs. 2 lakhs for retail investors).', 7, TRUE, NOW(), NOW()),
('What happens if an IPO is oversubscribed?', 'In case of oversubscription, shares are allocated proportionally among all applicants, or through a lottery system for retail investors.', 8, TRUE, NOW(), NOW());

-- Insert Django superuser (admin)
INSERT INTO auth_user (password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
('pbkdf2_sha256$600000$hash_here', TRUE, 'admin', 'Admin', 'User', 'admin@ipomanagement.com', TRUE, TRUE, NOW());

-- Insert Django content types
INSERT INTO django_content_type (app_label, model) VALUES
('ipo', 'company'),
('ipo', 'ipo'),
('ipo', 'document'),
('ipo', 'faq'),
('auth', 'user'),
('auth', 'group'),
('auth', 'permission'),
('admin', 'log'),
('contenttypes', 'contenttype'),
('sessions', 'session');

-- =====================================================
-- VIEWS FOR ANALYTICS
-- =====================================================

-- View for IPO statistics
CREATE VIEW ipo_statistics AS
SELECT 
    COUNT(*) as total_ipos,
    COUNT(CASE WHEN status = 'upcoming' THEN 1 END) as upcoming_ipos,
    COUNT(CASE WHEN status = 'ongoing' THEN 1 END) as ongoing_ipos,
    COUNT(CASE WHEN status = 'listed' THEN 1 END) as listed_ipos,
    AVG(CASE WHEN status = 'listed' THEN listing_gain END) as avg_listing_gain,
    AVG(CASE WHEN status = 'listed' THEN current_return END) as avg_current_return
FROM (
    SELECT 
        *,
        CASE 
            WHEN ipo_price > 0 AND listing_price > 0 
            THEN ((listing_price - ipo_price) / ipo_price) * 100 
            ELSE NULL 
        END as listing_gain,
        CASE 
            WHEN ipo_price > 0 AND current_market_price > 0 
            THEN ((current_market_price - ipo_price) / ipo_price) * 100 
            ELSE NULL 
        END as current_return
    FROM ipo_ipo
) ipos;

-- View for company IPO history
CREATE VIEW company_ipo_history AS
SELECT 
    c.id as company_id,
    c.name as company_name,
    c.logo as company_logo,
    i.id as ipo_id,
    i.price_band_lower,
    i.price_band_upper,
    i.open_date,
    i.close_date,
    i.issue_size,
    i.issue_type,
    i.listing_date,
    i.status,
    i.ipo_price,
    i.listing_price,
    i.current_market_price,
    CASE 
        WHEN i.ipo_price > 0 AND i.listing_price > 0 
        THEN ((i.listing_price - i.ipo_price) / i.ipo_price) * 100 
        ELSE NULL 
    END as listing_gain,
    CASE 
        WHEN i.ipo_price > 0 AND i.current_market_price > 0 
        THEN ((i.current_market_price - i.ipo_price) / i.ipo_price) * 100 
        ELSE NULL 
    END as current_return
FROM ipo_company c
LEFT JOIN ipo_ipo i ON c.id = i.company_id
ORDER BY c.name, i.open_date DESC;

-- =====================================================
-- COMMENTS AND DOCUMENTATION
-- =====================================================

COMMENT ON TABLE ipo_company IS 'Stores company information including name and logo';
COMMENT ON TABLE ipo_ipo IS 'Stores IPO details including pricing, dates, and status';
COMMENT ON TABLE ipo_document IS 'Stores IPO-related documents (RHP and DRHP)';
COMMENT ON TABLE ipo_faq IS 'Stores frequently asked questions for the IPO system';

COMMENT ON COLUMN ipo_ipo.price_band_lower IS 'Lower limit of the IPO price band';
COMMENT ON COLUMN ipo_ipo.price_band_upper IS 'Upper limit of the IPO price band';
COMMENT ON COLUMN ipo_ipo.issue_size IS 'Total issue size in crores';
COMMENT ON COLUMN ipo_ipo.ipo_price IS 'Final IPO price determined after book building';
COMMENT ON COLUMN ipo_ipo.listing_price IS 'Price at which the stock listed on exchange';
COMMENT ON COLUMN ipo_ipo.current_market_price IS 'Current market price of the stock';

-- =====================================================
-- GRANTS (if using separate user)
-- =====================================================

-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ipo_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ipo_user;
-- GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO ipo_user;

-- =====================================================
-- END OF DATABASE SCHEMA AND SAMPLE DATA
-- ===================================================== 