from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import UserFavorites, Franchise, Franchisor, Franchisee
import json

class FavoritesTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.franchisor_user = User.objects.create_user(username='franchisor', password='testpass123')
        
        # Create franchisor
        self.franchisor = Franchisor.objects.create(
            user=self.franchisor_user,
            company_name='Test Company'
        )
        
        # Create franchisee
        self.franchisee = Franchisee.objects.create(
            user=self.user,
            business_name='Test Business'
        )
        
        # Create test franchises
        self.franchise1 = Franchise.objects.create(
            franchisor=self.franchisor,
            name='Test Franchise 1',
            category='Food',
            investment=100000,
            description='Test description',
            status='approved',
            is_active=True
        )
        
        self.franchise2 = Franchise.objects.create(
            franchisor=self.franchisor,
            name='Test Franchise 2',
            category='Retail',
            investment=200000,
            description='Test description 2',
            status='approved',
            is_active=True
        )
        
        self.client = Client()
    
    def test_add_favorite(self):
        """Test adding a franchise to favorites"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('toggle_favorite', args=[self.franchise1.id]),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'added')
        self.assertTrue(data['is_favorited'])
        
        # Verify favorite was created
        favorite_exists = UserFavorites.objects.filter(
            user=self.user,
            franchise=self.franchise1
        ).exists()
        self.assertTrue(favorite_exists)
    
    def test_remove_favorite(self):
        """Test removing a franchise from favorites"""
        self.client.login(username='testuser', password='testpass123')
        
        # First add to favorites
        UserFavorites.objects.create(
            user=self.user,
            franchise=self.franchise1
        )
        
        # Then remove
        response = self.client.post(
            reverse('toggle_favorite', args=[self.franchise1.id]),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'removed')
        self.assertFalse(data['is_favorited'])
        
        # Verify favorite was deleted
        favorite_exists = UserFavorites.objects.filter(
            user=self.user,
            franchise=self.franchise1
        ).exists()
        self.assertFalse(favorite_exists)
    
    def test_view_favorites_list(self):
        """Test viewing favorites page"""
        self.client.login(username='testuser', password='testpass123')
        
        # Add some favorites
        UserFavorites.objects.create(user=self.user, franchise=self.franchise1)
        UserFavorites.objects.create(user=self.user, franchise=self.franchise2)
        
        response = self.client.get(reverse('favorites'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Franchise 1')
        self.assertContains(response, 'Test Franchise 2')
        self.assertEqual(response.context['total_count'], 2)
    
    def test_favorites_persistence(self):
        """Test that favorites persist across sessions"""
        self.client.login(username='testuser', password='testpass123')
        
        # Add favorite
        UserFavorites.objects.create(user=self.user, franchise=self.franchise1)
        
        # Logout and login again
        self.client.logout()
        self.client.login(username='testuser', password='testpass123')
        
        # Check if favorite still exists
        favorite_exists = UserFavorites.objects.filter(
            user=self.user,
            franchise=self.franchise1
        ).exists()
        self.assertTrue(favorite_exists)
    
    def test_check_favorite_status(self):
        """Test checking if franchise is favorited"""
        self.client.login(username='testuser', password='testpass123')
        
        # Check unfavorited franchise
        response = self.client.get(reverse('check_favorite', args=[self.franchise1.id]))
        data = json.loads(response.content)
        self.assertFalse(data['is_favorited'])
        
        # Add to favorites
        UserFavorites.objects.create(user=self.user, franchise=self.franchise1)
        
        # Check again
        response = self.client.get(reverse('check_favorite', args=[self.franchise1.id]))
        data = json.loads(response.content)
        self.assertTrue(data['is_favorited'])
    
    def test_duplicate_favorite_prevention(self):
        """Test that duplicate favorites are prevented"""
        self.client.login(username='testuser', password='testpass123')
        
        # Add favorite twice
        UserFavorites.objects.create(user=self.user, franchise=self.franchise1)
        
        # Try to add again - should not create duplicate
        with self.assertRaises(Exception):
            UserFavorites.objects.create(user=self.user, franchise=self.franchise1)
        
        # Verify only one exists
        count = UserFavorites.objects.filter(
            user=self.user,
            franchise=self.franchise1
        ).count()
        self.assertEqual(count, 1)
    
    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access favorites"""
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_empty_favorites_page(self):
        """Test favorites page with no favorites"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('favorites'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Favorites Yet')
        self.assertEqual(response.context['total_count'], 0)
