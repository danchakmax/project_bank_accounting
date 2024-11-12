import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from banking_system import UserInterface, UserManager


class TestLoanSystem(unittest.TestCase):
    def setUp(self):
        self.user_manager = UserManager()
        self.user_interface = UserInterface(None, self.user_manager, None)

        self.user_interface.current_user_data = {
            "name": "Test User",
            "phone": "+380123456789",
            "salary": 5000,
            "balance": 1000,
            "loan_amount": 0,
            "loan_start_date": datetime.now().strftime("%Y-%m-%d"),
            "loan_due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "interest_rate": 1.01,
            "transactions": [],
        }

    @patch('tkinter.messagebox.showerror')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.simpledialog.askinteger', side_effect=[2000, 7])
    def test_apply_for_loan_successful(self, mock_askinteger, mock_showinfo, mock_showerror):
        self.user_interface.apply_for_loan()
        self.assertEqual(self.user_interface.current_user_data["loan_amount"], 2000)
        self.assertEqual(self.user_interface.current_user_data["balance"], 3000)

    @patch('tkinter.messagebox.showerror')
    def test_apply_for_loan_existing_loan(self, mock_showerror):
        # Тест на спробу отримання кредиту, маючи активний кредит
        self.user_interface.current_user_data["loan_amount"] = 1000
        self.user_interface.apply_for_loan()
        mock_showerror.assert_called_once_with("Loan Denied",
                                               "You already have an active loan. Please repay it before applying for a new one.")
        self.assertEqual(self.user_interface.current_user_data["loan_amount"], 1000)

    @patch('tkinter.messagebox.showerror')
    @patch('tkinter.simpledialog.askinteger', return_value=6000)
    def test_apply_for_loan_exceeds_max(self, mock_askinteger, mock_showerror):
        self.user_interface.apply_for_loan()
        mock_showerror.assert_called_once_with("Loan Denied",
                                               "Loan amount exceeds limit! Maximum loan amount is 5000.")
        self.assertEqual(self.user_interface.current_user_data["loan_amount"], 0)

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.simpledialog.askinteger', return_value=2000)
    def test_repay_loan_full(self, mock_askinteger, mock_showinfo):
        self.user_interface.current_user_data["loan_amount"] = 2000
        self.user_interface.current_user_data["balance"] = 3000
        self.user_interface.repay_loan()
        self.assertEqual(self.user_interface.current_user_data["loan_amount"], 0)
        self.assertEqual(self.user_interface.current_user_data["balance"], 1000)
        self.assertIn("Loan fully repaid: -2000", self.user_interface.current_user_data["transactions"])

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.simpledialog.askinteger', return_value=1000)
    def test_repay_loan_partial(self, mock_askinteger, mock_showinfo):
        self.user_interface.current_user_data["loan_amount"] = 2000
        self.user_interface.current_user_data["balance"] = 3000
        self.user_interface.repay_loan()
        self.assertEqual(self.user_interface.current_user_data["loan_amount"], 1000)
        self.assertEqual(self.user_interface.current_user_data["balance"], 2000)
        self.assertIn("Partial loan repayment: -1000", self.user_interface.current_user_data["transactions"])

    @patch('tkinter.messagebox.showinfo')
    def test_repay_loan_no_active_loan(self, mock_showinfo):
        self.user_interface.current_user_data["loan_amount"] = 0
        self.user_interface.repay_loan()
        mock_showinfo.assert_called_once_with("No Active Loan", "You have no active loan to repay.")

    def test_update_loan_interest_no_overdue(self):
        self.user_interface.current_user_data["loan_amount"] = 1000
        self.user_interface.current_user_data["loan_start_date"] = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        self.user_interface.current_user_data["interest_rate"] = 1.01
        self.user_interface.update_loan_interest()
        expected_loan_amount = 1000 * (1.01 ** 5)
        self.assertAlmostEqual(self.user_interface.current_user_data["loan_amount"], round(expected_loan_amount, 2))

    def test_update_loan_interest_with_overdue(self):
        self.user_interface.current_user_data["loan_amount"] = 1000
        self.user_interface.current_user_data["loan_start_date"] = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        self.user_interface.current_user_data["loan_due_date"] = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        self.user_interface.current_user_data["interest_rate"] = 1.01
        self.user_interface.update_loan_interest()
        expected_loan_amount = 1000 * (1.01 ** 10) * (1.1 ** 3)
        self.assertAlmostEqual(self.user_interface.current_user_data["loan_amount"], round(expected_loan_amount, 2))
        self.assertIn("Penalty added for 3 overdue days.", self.user_interface.current_user_data["transactions"])


if __name__ == '__main__':
    unittest.main()
