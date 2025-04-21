from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Label, Note, Trash_Bin
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError


class BaseTestCase(APITestCase):
    def setUp(self):
       
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
      
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

      
        self.label = Label.objects.create(
            user=self.user, 
            title='Test Label',
            is_trashed=False
        )

        self.note1 = Note.objects.create(
            user=self.user,  
            label=self.label,
            context='Test Note 1',
            status=Note.PROCESSING,
            is_completed=False,
            is_pinned=False,
            is_trashed=False
        )


class LabelTests(BaseTestCase):
    def test_create_label(self):
        response = self.client.post('/api/v1/labels/create/', {'title': 'New Label'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Label.objects.count(), 2)

    def test_create_label_invalid_data(self):
        response = self.client.post('/api/v1/labels/create/', {'title': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_labels(self):
        response = self.client.get('/api/v1/labels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_label_detail(self):
        response = self.client.get(f'/api/v1/labels/{self.label.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Label')

    def test_label_detail_not_found(self):
        response = self.client.get('/api/v1/labels/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_label(self):
        response = self.client.patch(f'/api/v1/labels/{self.label.id}/', {'title': 'Updated Label'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.label.refresh_from_db()
        self.assertEqual(self.label.title, 'Updated Label')

    def test_move_label_to_trash(self):
        response = self.client.post(f'/api/v1/labels/{self.label.id}/trash/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.label.refresh_from_db()
        self.assertTrue(self.label.is_trashed)


class NoteTests(BaseTestCase):
   def test_create_note(self):
    response = self.client.post('/api/v1/notes/create/', {
        'context': 'New Note',
        'label': self.label.id,
        'status': Note.PROCESSING
    })
    print(response.data)  

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Note.objects.count(), 2)
    def test_create_note_invalid_data(self):
        response = self.client.post('/api/v1/notes/create/', {'context': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_notes(self):
        response = self.client.get('/api/v1/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_note_detail(self):
        response = self.client.get(f'/api/v1/notes/{self.note1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['context'], 'Test Note 1')

    def test_note_detail_not_found(self):
        response = self.client.get('/api/v1/notes/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_note(self):
        response = self.client.patch(f'/api/v1/notes/{self.note1.id}/', {
            'context': 'Updated Note',
            'status': Note.COMPLETED
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.context, 'Updated Note')

    def test_pin_note(self):
        response = self.client.patch(f'/api/v1/notes/{self.note1.id}/', {'is_pinned': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note1.refresh_from_db()
        self.assertTrue(self.note1.is_pinned)

    def test_pin_limit_exceeded(self):
        for i in range(10):
            Note.objects.create(
                user=self.user, 
                label=self.label,
                context=f'Note {i}',
                status=Note.PROCESSING,
                is_pinned=True,
                is_trashed=False
            )
        response = self.client.patch(f'/api/v1/notes/{self.note1.id}/', {'is_pinned': True})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_notes_for_label(self):
        response = self.client.get(f'/api/v1/labels/{self.label.id}/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_move_note_to_trash(self):
        response = self.client.post(f'/api/v1/notes/{self.note1.id}/trash/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note1.refresh_from_db()
        self.assertTrue(self.note1.is_trashed)


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.label = Label.objects.create(user=self.user, title='Test Label', is_trashed=False)
        self.note = Note.objects.create(
            user=self.user,  
            label=self.label,
            context='Test Note',
            status=Note.PROCESSING,
            is_completed=False,
            is_pinned=False,
            is_trashed=False
        )

    def test_label_str(self):
        self.assertEqual(str(self.label), 'Label name: Test Label')

    def test_note_str(self):
        self.assertEqual(str(self.note), 'Test Note')

    def test_trash_bin_str(self):
        trash_bin = Trash_Bin.objects.create(user=self.user, note=self.note)
        self.assertEqual(str(trash_bin), 'Test Note')

    def test_trash_bin_days_left(self):
        trash_bin = Trash_Bin.objects.create(user=self.user, note=self.note)
        self.assertGreaterEqual(trash_bin.days_left(), 29)

    def test_trash_bin_clean_method(self):
        trash_bin = Trash_Bin(user=self.user)
        with self.assertRaises(ValidationError):
            trash_bin.clean()

    def test_trash_bin_unique_constraint(self):
        Trash_Bin.objects.create(user=self.user, note=self.note)
        with self.assertRaises(Exception):
            Trash_Bin.objects.create(user=self.user, note=self.note)


class TrashBinTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.note1.is_trashed = True
        self.note1.save()
        self.label.is_trashed = True
        self.label.save()
        self.trash_bin_note = Trash_Bin.objects.create(user=self.user, note=self.note1)
        self.trash_bin_label = Trash_Bin.objects.create(user=self.user, label=self.label)

    def test_list_trashed_notes(self):
        response = self.client.get('/api/v1/trash/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_trashed_labels(self):
        response = self.client.get('/api/v1/trash/labels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_trashed_note_detail(self):
        response = self.client.get(f'/api/v1/trash/notes/{self.note1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trashed_label_detail(self):
        response = self.client.get(f'/api/v1/trash/labels/{self.label.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_restore_note_from_trash(self):
        response = self.client.post(f'/api/v1/trash/notes/{self.note1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note1.refresh_from_db()
        self.assertFalse(self.note1.is_trashed)

    def test_restore_label_from_trash(self):
        response = self.client.post(f'/api/v1/trash/labels/{self.label.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.label.refresh_from_db()
        self.assertFalse(self.label.is_trashed)

    def test_filter_trashed_notes(self):
        response = self.client.get('/api/v1/trash/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['is_trashed'] for item in response.data['results']))

    def test_filter_trashed_labels(self):
        response = self.client.get('/api/v1/trash/labels/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(item['is_trashed'] for item in response.data['results']))