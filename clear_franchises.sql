-- ========================================
-- Clear Franchises and Applications Script
-- Safe deletion with foreign key ordering
-- ========================================

-- Start transaction for safety
BEGIN;

-- Step 1: Delete all notifications related to franchises
DELETE FROM notification WHERE related_franchise_id IS NOT NULL;

-- Step 2: Delete all franchise applications first (child table)
-- This must be done before deleting franchises due to foreign key constraints
DELETE FROM franchise_application;

-- Step 3: Delete all user favorites (references franchises)
DELETE FROM user_favorites;

-- Step 4: Now safe to delete all franchises (parent table)
DELETE FROM franchise;

-- Verify deletions
SELECT 'Remaining Franchises:' AS info, COUNT(*) AS count FROM franchise;
SELECT 'Remaining Applications:' AS info, COUNT(*) AS count FROM franchise_application;
SELECT 'Remaining Favorites:' AS info, COUNT(*) AS count FROM user_favorites;
SELECT 'Remaining Notifications:' AS info, COUNT(*) AS count FROM notification WHERE related_franchise_id IS NOT NULL;

-- If everything looks good, commit the transaction
-- COMMIT;

-- If something went wrong, rollback instead
-- ROLLBACK;

-- ========================================
-- INSTRUCTIONS:
-- ========================================
-- 1. Review the DELETE statements above
-- 2. The transaction starts with BEGIN
-- 3. After running, check the SELECT results
-- 4. If counts look correct, run: COMMIT;
-- 5. If something is wrong, run: ROLLBACK;
--
-- IMPORTANT: This script is wrapped in a transaction
-- so nothing is permanent until you COMMIT.
-- ========================================
