import unittest
from unittest.mock import patch, MagicMock, mock_open
import datetime
import random

# Set a fake environment variable to avoid display errors in headless environments
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Import the real pygame library
import pygame

# Mock the parts of pygame that are not needed for testing
pygame_mock = MagicMock()
pygame_mock.Rect = pygame.Rect  # Use the real Rect class
pygame_mock.K_w = pygame.K_w
pygame_mock.K_s = pygame.K_s
pygame_mock.K_UP = pygame.K_UP
pygame_mock.K_DOWN = pygame.K_DOWN

import sys
sys.modules['pygame'] = pygame_mock

from main import (
    Particle,
    BallTrail,
    ScreenShake,
    save_score,
    GameState,
    handle_paddle_movement,
    handle_ball_collision,
    handle_scoring,
    PADDLE_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WINNING_SCORE,
)

class TestGameState(unittest.TestCase):
    def test_initialization(self):
        game_state = GameState("medium", "left")
        self.assertEqual(game_state.difficulty, "medium")
        self.assertEqual(game_state.player_side, "left")
        self.assertEqual(game_state.score_a, 0)
        self.assertEqual(game_state.score_b, 0)
        self.assertIn(abs(game_state.ball_speed_x), [6])
        self.assertIn(abs(game_state.ball_speed_y), [6])

class TestGameLogic(unittest.TestCase):

    def setUp(self):
        # Mock random to have predictable outcomes
        random.choice = MagicMock(return_value=1)
        random.uniform = MagicMock(return_value=0.5)
        random.randint = MagicMock(return_value=1)

        # Initialize a fresh GameState for each test
        self.game_state = GameState("medium", "left")

        # Mock keys pressed
        self.keys = {pygame.K_w: False, pygame.K_s: False, pygame.K_UP: False, pygame.K_DOWN: False}

    def test_player_paddle_movement_up(self):
        self.game_state.player_side = "left"
        initial_y = self.game_state.paddle_a.y
        self.keys[pygame.K_w] = True
        handle_paddle_movement(self.keys, self.game_state)
        self.assertEqual(self.game_state.paddle_a.y, initial_y - PADDLE_SPEED)

    def test_player_paddle_movement_down(self):
        self.game_state.player_side = "left"
        initial_y = self.game_state.paddle_a.y
        self.keys[pygame.K_s] = True
        handle_paddle_movement(self.keys, self.game_state)
        self.assertEqual(self.game_state.paddle_a.y, initial_y + PADDLE_SPEED)

    def test_paddle_boundary_top(self):
        self.game_state.paddle_a.top = 0
        self.keys[pygame.K_w] = True
        handle_paddle_movement(self.keys, self.game_state)
        self.assertEqual(self.game_state.paddle_a.top, 0)

    def test_paddle_boundary_bottom(self):
        self.game_state.paddle_a.bottom = SCREEN_HEIGHT
        self.keys[pygame.K_s] = True
        handle_paddle_movement(self.keys, self.game_state)
        self.assertEqual(self.game_state.paddle_a.bottom, SCREEN_HEIGHT)

    def test_ai_paddle_movement(self):
        self.game_state.player_side = "left"
        self.game_state.paddle_b.centery = 300
        self.game_state.ball.centery = 400
        initial_y = self.game_state.paddle_b.y
        handle_paddle_movement(self.keys, self.game_state)
        self.assertEqual(self.game_state.paddle_b.y, initial_y + PADDLE_SPEED)

        self.game_state.ball.centery = 200
        handle_paddle_movement(self.keys, self.game_state)
        self.assertEqual(self.game_state.paddle_b.y, initial_y)

    def test_ball_wall_collision(self):
        self.game_state.ball.top = 0
        self.game_state.ball_speed_y = -5
        handle_ball_collision(self.game_state, ScreenShake(), [], "neon")
        self.assertEqual(self.game_state.ball_speed_y, 5)

        self.game_state.ball.bottom = SCREEN_HEIGHT
        self.game_state.ball_speed_y = 5
        handle_ball_collision(self.game_state, ScreenShake(), [], "neon")
        self.assertEqual(self.game_state.ball_speed_y, -5)

    def test_ball_paddle_collision(self):
        # Position ball to collide with paddle_b (moving right)
        self.game_state.ball_speed_x = 6
        self.game_state.ball.right = self.game_state.paddle_b.left
        self.game_state.ball.centery = self.game_state.paddle_b.centery
        initial_speed = self.game_state.ball_speed_x
        handle_ball_collision(self.game_state, ScreenShake(), [], "neon")
        self.assertEqual(self.game_state.ball_speed_x, -initial_speed)

        # Position ball to collide with paddle_a (moving left)
        self.game_state.ball_speed_x = -6
        self.game_state.ball.left = self.game_state.paddle_a.right
        self.game_state.ball.centery = self.game_state.paddle_a.centery
        initial_speed = self.game_state.ball_speed_x
        handle_ball_collision(self.game_state, ScreenShake(), [], "neon")
        self.assertEqual(self.game_state.ball_speed_x, -initial_speed)

    def test_scoring_player_a(self):
        self.game_state.ball.right = SCREEN_WIDTH + 1
        winner, scored = handle_scoring(self.game_state, [], "neon")
        self.assertEqual(self.game_state.score_a, 1)
        self.assertTrue(scored)
        self.assertIsNone(winner)

    def test_scoring_player_b(self):
        self.game_state.ball.left = -1
        winner, scored = handle_scoring(self.game_state, [], "neon")
        self.assertEqual(self.game_state.score_b, 1)
        self.assertTrue(scored)
        self.assertIsNone(winner)

    @patch('main.save_score')
    def test_win_condition(self, mock_save_score):
        self.game_state.score_a = WINNING_SCORE - 1
        self.game_state.ball.right = SCREEN_WIDTH + 1
        winner, _ = handle_scoring(self.game_state, [], "neon")
        self.assertEqual(winner, "Player A")
        mock_save_score.assert_called_once_with("Player A", WINNING_SCORE, 0)

class TestParticle(unittest.TestCase):

    def setUp(self):
        random.uniform = MagicMock(return_value=0.5)

    def test_init(self):
        particle = Particle(10, 20, (255, 0, 0))
        self.assertEqual(particle.x, 10)
        self.assertEqual(particle.y, 20)
        self.assertEqual(particle.color, (255, 0, 0))
        self.assertAlmostEqual(particle.velocity_x, 0.5)
        self.assertAlmostEqual(particle.velocity_y, 0.5)
        self.assertEqual(particle.life, 60)
        self.assertEqual(particle.max_life, 60)
        self.assertAlmostEqual(particle.size, 0.5)

    def test_update(self):
        particle = Particle(10, 20, (255, 0, 0))
        particle.velocity_x = 1
        particle.velocity_y = 1
        particle.update()
        self.assertEqual(particle.x, 11)
        self.assertEqual(particle.y, 21)
        self.assertEqual(particle.life, 59)
        self.assertAlmostEqual(particle.velocity_x, 0.98)
        self.assertAlmostEqual(particle.velocity_y, 0.98)

class TestBallTrail(unittest.TestCase):

    def test_update(self):
        trail = BallTrail()
        trail.max_length = 8
        # Add 8 positions
        for i in range(8):
            trail.update(i, i)
        self.assertEqual(len(trail.positions), 8)
        self.assertEqual(trail.positions[0], (0, 0))
        # Add one more, should pop the first one
        trail.update(8, 8)
        self.assertEqual(len(trail.positions), 8)
        self.assertEqual(trail.positions[0], (1, 1))


class TestScreenShake(unittest.TestCase):

    def setUp(self):
        random.randint = MagicMock(return_value=1)

    def test_add_shake(self):
        shake = ScreenShake()
        shake.add_shake(5, 10)
        self.assertEqual(shake.shake_intensity, 5)
        self.assertEqual(shake.shake_duration, 10)
        shake.add_shake(3, 12)
        self.assertEqual(shake.shake_intensity, 5)
        self.assertEqual(shake.shake_duration, 12)
        shake.add_shake(8, 8)
        self.assertEqual(shake.shake_intensity, 8)
        self.assertEqual(shake.shake_duration, 12)

    def test_update(self):
        shake = ScreenShake()
        shake.add_shake(5, 2)
        shake.update()
        self.assertEqual(shake.shake_duration, 1)
        self.assertEqual(shake.shake_intensity, 5)
        shake.update()
        self.assertEqual(shake.shake_duration, 0)
        self.assertEqual(shake.shake_intensity, 0)

    def test_get_offset(self):
        shake = ScreenShake()
        self.assertEqual(shake.get_offset(), (0, 0))
        shake.add_shake(5, 1)
        self.assertEqual(shake.get_offset(), (1, 1))
        random.randint.assert_called_with(-5, 5)

class TestSaveScore(unittest.TestCase):

    @patch('main.datetime')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_score(self, mock_file, mock_datetime):
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)
        save_score("Player A", 5, 2)
        mock_file.assert_called_with("scores.txt", "a")
        handle = mock_file()
        handle.write.assert_called_once_with("Date: 2023-01-01 12:00:00, Winner: Player A, Score: 5 - 2\n")

if __name__ == '__main__':
    unittest.main()