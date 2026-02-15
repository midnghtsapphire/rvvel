-- ============================================================================
-- Database Schema — Audrey Evans Official / GlowStarLabs
-- All tables for the production platform
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- 1. USERS
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    full_name VARCHAR(255),
    avatar_url TEXT,
    auth_provider VARCHAR(50) DEFAULT 'email',
    auth_provider_id VARCHAR(255),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'moderator')),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    -- Accessibility preferences (Standards 1, 3, 7)
    preferences JSONB DEFAULT '{
        "blue_light_filter": true,
        "dark_mode": true,
        "night_mode": false,
        "focus_mode": false,
        "reduced_motion": false,
        "high_contrast": false,
        "font_size": "medium",
        "break_reminder_minutes": 25,
        "visual_only_notifications": true,
        "interface_density": "comfortable"
    }'::jsonb,
    -- Location for GPS-based personalization
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    timezone VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_auth_provider ON users(auth_provider, auth_provider_id);

-- ============================================================================
-- 2. SUBSCRIPTIONS
-- ============================================================================
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    tier VARCHAR(20) DEFAULT 'free' CHECK (tier IN ('free', 'starter', 'pro', 'business', 'enterprise')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'canceled', 'past_due', 'trialing', 'paused')),
    tokens_remaining INTEGER DEFAULT 10,
    tokens_used INTEGER DEFAULT 0,
    current_period_start TIMESTAMPTZ,
    current_period_end TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe ON subscriptions(stripe_customer_id);

-- ============================================================================
-- 3. SKIN ANALYSES
-- ============================================================================
CREATE TABLE IF NOT EXISTS skin_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    image_url TEXT,
    skin_type VARCHAR(50),
    conditions JSONB DEFAULT '[]'::jsonb,
    hydration_level VARCHAR(20),
    sun_damage_score DECIMAL(3,1),
    texture_score DECIMAL(3,1),
    overall_score DECIMAL(3,1),
    ai_analysis TEXT,
    ai_model_used VARCHAR(100),
    -- GPS-based weather data at time of analysis
    weather_data JSONB,
    location_data JSONB,
    recommendations JSONB DEFAULT '[]'::jsonb,
    -- Carbon tracking (Standard 2)
    api_calls_made INTEGER DEFAULT 0,
    tokens_consumed INTEGER DEFAULT 0,
    co2_grams DECIMAL(10,4) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_skin_analyses_user ON skin_analyses(user_id);
CREATE INDEX idx_skin_analyses_date ON skin_analyses(created_at DESC);

-- ============================================================================
-- 4. PRODUCT RECOMMENDATIONS
-- ============================================================================
CREATE TABLE IF NOT EXISTS product_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID REFERENCES skin_analyses(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    product_name VARCHAR(255) NOT NULL,
    brand VARCHAR(255),
    category VARCHAR(100),
    description TEXT,
    price DECIMAL(10,2),
    affiliate_url TEXT,
    affiliate_tag VARCHAR(100),
    image_url TEXT,
    alt_text VARCHAR(500),  -- Standard 7: Alt text everywhere
    rating DECIMAL(3,1),
    match_score DECIMAL(3,1),
    skin_types JSONB DEFAULT '[]'::jsonb,
    conditions_addressed JSONB DEFAULT '[]'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_recommendations_user ON product_recommendations(user_id);
CREATE INDEX idx_recommendations_analysis ON product_recommendations(analysis_id);

-- ============================================================================
-- 5. AFFILIATE LINKS
-- ============================================================================
CREATE TABLE IF NOT EXISTS affiliate_links (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES product_recommendations(id) ON DELETE SET NULL,
    original_url TEXT NOT NULL,
    affiliate_url TEXT NOT NULL,
    affiliate_tag VARCHAR(100),
    platform VARCHAR(50) DEFAULT 'amazon',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- 6. AFFILIATE CLICKS
-- ============================================================================
CREATE TABLE IF NOT EXISTS affiliate_clicks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    link_id UUID REFERENCES affiliate_links(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    ip_address INET,
    user_agent TEXT,
    referrer TEXT,
    clicked_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_affiliate_clicks_link ON affiliate_clicks(link_id);
CREATE INDEX idx_affiliate_clicks_date ON affiliate_clicks(clicked_at DESC);

-- ============================================================================
-- 7. AFFILIATE CONVERSIONS
-- ============================================================================
CREATE TABLE IF NOT EXISTS affiliate_conversions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    click_id UUID REFERENCES affiliate_clicks(id) ON DELETE SET NULL,
    link_id UUID REFERENCES affiliate_links(id) ON DELETE SET NULL,
    order_amount DECIMAL(10,2),
    commission_amount DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'rejected')),
    converted_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- 8. AD PLACEMENTS (Selling Space)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ad_placements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    advertiser_id UUID REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url TEXT,
    alt_text VARCHAR(500) NOT NULL,  -- Standard 7: Alt text required
    target_url TEXT NOT NULL,
    placement_location VARCHAR(100) NOT NULL,
    tier VARCHAR(20) DEFAULT 'basic',
    price_monthly DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'paused', 'expired', 'rejected')),
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    targeting JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- 9. AD IMPRESSIONS
-- ============================================================================
CREATE TABLE IF NOT EXISTS ad_impressions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ad_id UUID REFERENCES ad_placements(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    page_url TEXT,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_ad_impressions_ad ON ad_impressions(ad_id);
CREATE INDEX idx_ad_impressions_date ON ad_impressions(recorded_at DESC);

-- ============================================================================
-- 10. AD CLICKS
-- ============================================================================
CREATE TABLE IF NOT EXISTS ad_clicks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ad_id UUID REFERENCES ad_placements(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    ip_address INET,
    clicked_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- 11. ROUTING RULES (Universal Data Router)
-- ============================================================================
CREATE TABLE IF NOT EXISTS routing_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    source_type VARCHAR(50) NOT NULL,
    source_pattern TEXT,
    destination_type VARCHAR(50) NOT NULL,
    destination_config JSONB NOT NULL,
    conditions JSONB DEFAULT '[]'::jsonb,
    priority INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    last_triggered_at TIMESTAMPTZ,
    trigger_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_routing_rules_user ON routing_rules(user_id);

-- ============================================================================
-- 12. ROUTED ITEMS
-- ============================================================================
CREATE TABLE IF NOT EXISTS routed_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_id UUID REFERENCES routing_rules(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    source_type VARCHAR(50),
    source_id VARCHAR(255),
    destination_type VARCHAR(50),
    destination_id VARCHAR(255),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'routed', 'failed', 'skipped')),
    metadata JSONB DEFAULT '{}'::jsonb,
    error_message TEXT,
    routed_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- 13. BENCHMARK METRICS (AI Benchmarking)
-- ============================================================================
CREATE TABLE IF NOT EXISTS benchmark_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id VARCHAR(255) NOT NULL,
    model_name VARCHAR(255) NOT NULL,
    provider VARCHAR(100),
    task_type VARCHAR(50) NOT NULL,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    latency_ms DECIMAL(10,2),
    cost_usd DECIMAL(10,6),
    quality_score DECIMAL(5,2),
    -- Carbon tracking (Standard 2)
    co2_grams DECIMAL(10,4),
    cached BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_benchmarks_model ON benchmark_metrics(model_id);
CREATE INDEX idx_benchmarks_date ON benchmark_metrics(created_at DESC);

-- ============================================================================
-- 14. THOUGHT CHAINS (Kimi thought-chain reuse)
-- ============================================================================
CREATE TABLE IF NOT EXISTS thought_chains (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    model_id VARCHAR(255),
    prompt_hash VARCHAR(64) NOT NULL,
    prompt_text TEXT NOT NULL,
    chain_data JSONB NOT NULL,
    response_text TEXT,
    tokens_used INTEGER,
    reuse_count INTEGER DEFAULT 0,
    -- Carbon savings from reuse (Standard 8)
    co2_saved_grams DECIMAL(10,4) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_reused_at TIMESTAMPTZ
);

CREATE INDEX idx_thought_chains_hash ON thought_chains(prompt_hash);
CREATE INDEX idx_thought_chains_reuse ON thought_chains(reuse_count DESC);

-- ============================================================================
-- 15. NOTIFICATIONS (Visual-only — Standard 7)
-- ============================================================================
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('info', 'success', 'warning', 'error', 'achievement', 'break_reminder')),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    -- Visual-only: icon, color, flash pattern (NO audio)
    icon VARCHAR(50),
    color VARCHAR(20),
    flash_pattern VARCHAR(20) DEFAULT 'none',
    action_url TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
CREATE INDEX idx_notifications_date ON notifications(created_at DESC);

-- ============================================================================
-- 16. ANALYTICS EVENTS
-- ============================================================================
CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{}'::jsonb,
    page_url TEXT,
    session_id VARCHAR(100),
    -- Carbon tracking (Standard 2)
    api_calls_in_session INTEGER DEFAULT 0,
    cached_responses_in_session INTEGER DEFAULT 0,
    co2_saved_grams DECIMAL(10,4) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_analytics_user ON analytics_events(user_id);
CREATE INDEX idx_analytics_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_date ON analytics_events(created_at DESC);

-- ============================================================================
-- 17. CARBON LEDGER (Standard 8: Carbon Savings Quantifier)
-- ============================================================================
CREATE TABLE IF NOT EXISTS carbon_ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action_type VARCHAR(100) NOT NULL,
    co2_produced_grams DECIMAL(10,4) DEFAULT 0,
    co2_saved_grams DECIMAL(10,4) DEFAULT 0,
    starbucks_cups_equivalent DECIMAL(10,4) DEFAULT 0,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_carbon_user ON carbon_ledger(user_id);
CREATE INDEX idx_carbon_date ON carbon_ledger(created_at DESC);

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables with updated_at
CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_subscriptions_updated_at BEFORE UPDATE ON subscriptions FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_ad_placements_updated_at BEFORE UPDATE ON ad_placements FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER trg_routing_rules_updated_at BEFORE UPDATE ON routing_rules FOR EACH ROW EXECUTE FUNCTION update_updated_at();
