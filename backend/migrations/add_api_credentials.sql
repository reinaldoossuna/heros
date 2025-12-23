-- API Credentials Table
-- Stores rotating API credentials securely with audit trail

CREATE TABLE IF NOT EXISTS api_credentials (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL,
    password_encrypted VARCHAR(255) NOT NULL,
    last_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT service_name_unique UNIQUE (service_name)
);

-- Audit table to track credential changes
CREATE TABLE IF NOT EXISTS api_credentials_audit (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(50) NOT NULL,
    action VARCHAR(20) NOT NULL,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100),
    previous_username VARCHAR(255),
    new_username VARCHAR(255),
    notes TEXT
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_api_credentials_service ON api_credentials(service_name);
CREATE INDEX IF NOT EXISTS idx_api_credentials_active ON api_credentials(is_active);
CREATE INDEX IF NOT EXISTS idx_api_credentials_audit_service ON api_credentials_audit(service_name);
CREATE INDEX IF NOT EXISTS idx_api_credentials_audit_date ON api_credentials_audit(changed_at DESC);

-- Trigger to log updates to audit table
CREATE OR REPLACE FUNCTION log_credential_update()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO api_credentials_audit 
        (service_name, action, changed_by, previous_username, new_username, notes)
        VALUES 
        (NEW.service_name, 'UPDATE', NEW.updated_by, OLD.username, NEW.username, 
         'Password updated. Last update: ' || NEW.last_updated);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER credential_update_trigger
AFTER UPDATE ON api_credentials
FOR EACH ROW
EXECUTE FUNCTION log_credential_update();

-- Insert default credentials (encrypted with a simple base64 for demo - use proper encryption in production)
-- Note: Replace these with actual encrypted credentials and update engtec settings
INSERT INTO api_credentials (service_name, username, password_encrypted, updated_by, is_active)
VALUES 
    ('engtec', 'ufms@eng.com', 'encrypted_password_here', 'system_init', false),
    ('noaa', 'paulo.t.oliveira@ufms.br', 'encrypted_password_here', 'system_init', true)
ON CONFLICT (service_name) DO NOTHING;
