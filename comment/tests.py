from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from comment.models import Comment
from news.models import Berita
from following.models import CabangOlahraga
import json


class CommentViewsTestCase(TestCase):
    """Comprehensive test suite for Comment app views"""
    
    def setUp(self):
        """Set up test data before each test method"""
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123',
            email='user1@test.com'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123',
            email='user2@test.com'
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@test.com'
        )
        
        # Create CabangOlahraga (required for Berita)
        self.cabang = CabangOlahraga.objects.create(
            name='Sepak Bola'
        )
        
        # Create test news
        self.berita = Berita.objects.create(
            title='Test News Article',
            content='This is test content for news article',
            category='event',
            author=self.user1,
            cabangOlahraga=self.cabang
        )
        
        # Create test comments
        self.comment1 = Comment.objects.create(
            news=self.berita,
            user=self.user1,
            content='This is a test comment from user1'
        )
        self.comment2 = Comment.objects.create(
            news=self.berita,
            user=self.user2,
            content='This is a test comment from user2'
        )
        
        # Initialize test client
        self.client = Client()
    
    # ========== Tests for show_json view ==========
    
    def test_show_json_success_anonymous(self):
        """Test showing comments as JSON for anonymous users"""
        url = reverse('comment:show_json', kwargs={'news_id': self.berita.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Should return 2 comments
        self.assertEqual(len(data), 2)
        
        # Check structure of first comment
        comment = data[0]
        self.assertIn('id', comment)
        self.assertIn('user', comment)
        self.assertIn('content', comment)
        self.assertIn('is_edited', comment)
        self.assertIn('date', comment)
        self.assertIn('is_owner', comment)
        self.assertIn('can_delete', comment)
        
        # Anonymous user should not be owner
        self.assertFalse(comment['is_owner'])
        self.assertFalse(comment['can_delete'])
    
    def test_show_json_success_authenticated(self):
        """Test showing comments as JSON for authenticated users"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:show_json', kwargs={'news_id': self.berita.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Find comment owned by user1
        user1_comment = next(c for c in data if c['user'] == 'testuser1')
        user2_comment = next(c for c in data if c['user'] == 'testuser2')
        
        # User1 should be owner of their own comment
        self.assertTrue(user1_comment['is_owner'])
        self.assertTrue(user1_comment['can_delete'])
        
        # User1 should NOT be owner of user2's comment
        self.assertFalse(user2_comment['is_owner'])
        self.assertFalse(user2_comment['can_delete'])
    
    def test_show_json_superuser_can_delete_all(self):
        """Test that superuser can delete any comment"""
        self.client.login(username='admin', password='adminpass123')
        url = reverse('comment:show_json', kwargs={'news_id': self.berita.id})
        response = self.client.get(url)
        
        data = json.loads(response.content)
        
        # Superuser should be able to delete all comments
        for comment in data:
            self.assertTrue(comment['can_delete'])
    
    def test_show_json_news_not_found(self):
        """Test show_json with non-existent news ID"""
        url = reverse('comment:show_json', kwargs={'news_id': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_show_json_ordered_by_created_at(self):
        """Test that comments are ordered by created_at descending"""
        # Create a new comment
        new_comment = Comment.objects.create(
            news=self.berita,
            user=self.user1,
            content='Latest comment'
        )
        
        url = reverse('comment:show_json', kwargs={'news_id': self.berita.id})
        response = self.client.get(url)
        data = json.loads(response.content)
        
        # First comment should be the newest one
        self.assertEqual(data[0]['id'], new_comment.id)
    
    # ========== Tests for add_comment view ==========
    
    def test_add_comment_requires_login(self):
        """Test that add_comment requires authentication"""
        url = reverse('comment:add_comment', kwargs={'news_id': self.berita.id})
        response = self.client.post(url, {'content': 'Test comment'})
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_add_comment_success(self):
        """Test successfully adding a comment"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:add_comment', kwargs={'news_id': self.berita.id})
        
        initial_count = Comment.objects.count()
        
        response = self.client.post(url, {
            'content': 'This is a new test comment'
        })
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        
        # Check response structure
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Comment added successfully.')
        self.assertIn('comment', data)
        
        # Check comment data
        comment_data = data['comment']
        self.assertEqual(comment_data['user'], 'testuser1')
        self.assertEqual(comment_data['content'], 'This is a new test comment')
        self.assertTrue(comment_data['is_owner'])
        self.assertFalse(comment_data['is_edited'])
        
        # Verify comment was created in database
        self.assertEqual(Comment.objects.count(), initial_count + 1)
    
    def test_add_comment_empty_content(self):
        """Test that empty comments are rejected"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:add_comment', kwargs={'news_id': self.berita.id})
        
        response = self.client.post(url, {'content': '   '})
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Comment cannot be empty.')
    
    def test_add_comment_news_not_found(self):
        """Test adding comment to non-existent news"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:add_comment', kwargs={'news_id': 99999})
        
        response = self.client.post(url, {'content': 'Test'})
        
        self.assertEqual(response.status_code, 404)
    
    def test_add_comment_requires_post(self):
        """Test that add_comment only accepts POST requests"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:add_comment', kwargs={'news_id': self.berita.id})
        
        response = self.client.get(url)
        
        # Should return 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)
    
    # ========== Tests for edit_comment view ==========
    
    def test_edit_comment_requires_login(self):
        """Test that edit_comment requires authentication"""
        url = reverse('comment:edit_comment', kwargs={'comment_id': self.comment1.id})
        response = self.client.post(url, {'content': 'Edited'})
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_edit_comment_success(self):
        """Test successfully editing own comment"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:edit_comment', kwargs={'comment_id': self.comment1.id})
        
        response = self.client.post(url, {
            'content': 'This is the edited comment content'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Check response
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Comment updated successfully.')
        self.assertEqual(data['comment']['content'], 'This is the edited comment content')
        self.assertTrue(data['comment']['is_edited'])
        
        # Verify in database
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.content, 'This is the edited comment content')
        self.assertTrue(self.comment1.is_edited)
    
    def test_edit_comment_no_change_not_marked_edited(self):
        """Test that unchanged content doesn't mark as edited"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:edit_comment', kwargs={'comment_id': self.comment1.id})
        
        original_content = self.comment1.content
        original_is_edited = self.comment1.is_edited
        
        response = self.client.post(url, {'content': original_content})
        
        self.assertEqual(response.status_code, 200)
        
        # Verify is_edited flag didn't change
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.is_edited, original_is_edited)
    
    def test_edit_comment_forbidden_other_user(self):
        """Test that users cannot edit other users' comments"""
        self.client.login(username='testuser2', password='testpass123')
        url = reverse('comment:edit_comment', kwargs={'comment_id': self.comment1.id})
        
        response = self.client.post(url, {'content': 'Trying to edit'})
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "You don't have permission to edit this comment.")
    
    def test_edit_comment_empty_content(self):
        """Test that empty content is rejected when editing"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:edit_comment', kwargs={'comment_id': self.comment1.id})
        
        response = self.client.post(url, {'content': '   '})
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Comment cannot be empty.')
    
    def test_edit_comment_not_found(self):
        """Test editing non-existent comment"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:edit_comment', kwargs={'comment_id': 99999})
        
        response = self.client.post(url, {'content': 'Test'})
        
        self.assertEqual(response.status_code, 404)
    
    # ========== Tests for delete_comment view ==========
    
    def test_delete_comment_requires_login(self):
        """Test that delete_comment requires authentication"""
        url = reverse('comment:delete_comment', kwargs={'comment_id': self.comment1.id})
        response = self.client.post(url)
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_delete_comment_success(self):
        """Test successfully deleting own comment"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:delete_comment', kwargs={'comment_id': self.comment1.id})
        
        initial_count = Comment.objects.count()
        comment_id = self.comment1.id
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Check response
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Comment deleted successfully.')
        
        # Verify deletion in database
        self.assertEqual(Comment.objects.count(), initial_count - 1)
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())
    
    def test_delete_comment_forbidden_other_user(self):
        """Test that users cannot delete other users' comments"""
        self.client.login(username='testuser2', password='testpass123')
        url = reverse('comment:delete_comment', kwargs={'comment_id': self.comment1.id})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertEqual(data['error'], "You don't have permission to delete this comment.")
        
        # Verify comment still exists
        self.assertTrue(Comment.objects.filter(id=self.comment1.id).exists())
    
    def test_delete_comment_superuser_can_delete_any(self):
        """Test that superuser can delete any comment"""
        self.client.login(username='admin', password='adminpass123')
        url = reverse('comment:delete_comment', kwargs={'comment_id': self.comment1.id})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # Verify deletion
        self.assertFalse(Comment.objects.filter(id=self.comment1.id).exists())
    
    def test_delete_comment_not_found(self):
        """Test deleting non-existent comment"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:delete_comment', kwargs={'comment_id': 99999})
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 404)
    
    def test_delete_comment_requires_post(self):
        """Test that delete_comment only accepts POST requests"""
        self.client.login(username='testuser1', password='testpass123')
        url = reverse('comment:delete_comment', kwargs={'comment_id': self.comment1.id})
        
        response = self.client.get(url)
        
        # Should return 405 Method Not Allowed
        self.assertEqual(response.status_code, 405)


class CommentModelTestCase(TestCase):
    """Test suite for Comment model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.cabang = CabangOlahraga.objects.create(name='Basketball')
        
        self.berita = Berita.objects.create(
            title='Test News',
            content='Test content',
            category='event',
            author=self.user,
            cabangOlahraga=self.cabang
        )
    
    def test_create_comment(self):
        """Test creating a comment"""
        comment = Comment.objects.create(
            news=self.berita,
            user=self.user,
            content='Test comment content'
        )
        
        self.assertEqual(comment.content, 'Test comment content')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.news, self.berita)
        self.assertFalse(comment.is_edited)
        self.assertIsNotNone(comment.created_at)
        self.assertIsNotNone(comment.updated_at)
    
    def test_comment_str_method(self):
        """Test comment string representation"""
        comment = Comment.objects.create(
            news=self.berita,
            user=self.user,
            content='This is a long comment that should be truncated'
        )
        
        str_repr = str(comment)
        self.assertTrue(str_repr.startswith('testuser:'))
        self.assertLessEqual(len(str_repr), 50)  # username + ': ' + 40 chars
    
    def test_comment_ordering(self):
        """Test that comments are ordered by created_at descending"""
        comment1 = Comment.objects.create(
            news=self.berita,
            user=self.user,
            content='First comment'
        )
        
        comment2 = Comment.objects.create(
            news=self.berita,
            user=self.user,
            content='Second comment'
        )
        
        comments = Comment.objects.all()
        self.assertEqual(comments[0].id, comment2.id)
        self.assertEqual(comments[1].id, comment1.id)
    
    def test_comment_cascade_delete_with_news(self):
        """Test that comments are deleted when news is deleted"""
        comment = Comment.objects.create(
            news=self.berita,
            user=self.user,
            content='Test comment'
        )
        
        comment_id = comment.id
        self.berita.delete()
        
        # Comment should be deleted
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())
    
    def test_comment_cascade_delete_with_user(self):
        """Test that comments are deleted when user is deleted"""
        comment = Comment.objects.create(
            news=self.berita,
            user=self.user,
            content='Test comment'
        )
        
        comment_id = comment.id
        self.user.delete()
        
        # Comment should be deleted
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())
    
    def test_comment_max_length(self):
        """Test comment content max length"""
        long_content = 'x' * 501  # Exceeds max_length of 500
        
        with self.assertRaises(Exception):
            comment = Comment.objects.create(
                news=self.berita,
                user=self.user,
                content=long_content
            )
            comment.full_clean()  # This will raise ValidationError