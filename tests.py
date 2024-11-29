import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from banking_system import UserInterface, UserManager


class TestLoanSystem(unittest.TestCase):
    def setUp(self):
        self.mock_master = MagicMock()
        self.mock_master.winfo_children.return_value = []

        self.mock_manager = UserManager()
        self.mock_manager.users = {
            "+380123456789": {
                "name": "Test User",
                "phone": "+380123456789",
                "salary": 5000,
                "balance": 1000,
                "loan_amount": 0,
                "loan_start_date": datetime.now().strftime("%Y-%m-%d"),
                "loan_due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "interest_rate": 1.01,
                "transactions": []
            }
        }
        self.user_interface = UserInterface(self.mock_master, self.mock_manager, None)
        self.user_interface.current_user_data = self.mock_manager.users["+380123456789"]

    @patch('tkinter.messagebox.showerror')
    def test_apply_for_loan_existing_loan(self, mock_showerror):
        # Тест активного кредиту
        self.user_interface.current_user_data["loan_amount"] = 1000
        self.user_interface.apply_for_loan()
        mock_showerror.assert_called_once_with("Loan Denied",
                                               "You already have an active loan. Please repay it before applying for a new one.")

    @patch('tkinter.messagebox.showerror')
    @patch('tkinter.simpledialog.askinteger', return_value=6000)
    def test_apply_for_loan_exceeds_max(self, mock_askinteger, mock_showerror):
        self.user_interface.apply_for_loan()
        mock_showerror.assert_called_once_with("Loan Denied", "Loan amount exceeds limit! Maximum loan amount is 5000.")

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.simpledialog.askinteger', return_value=2000)
    def test_repay_loan_full(self, mock_askinteger, mock_showinfo):
        self.user_interface.current_user_data["loan_amount"] = 2000
        self.user_interface.current_user_data["balance"] = 3000
        self.user_interface.repay_loan()
        self.assertEqual(self.user_interface.current_user_data["loan_amount"], 0)
        self.assertEqual(self.user_interface.current_user_data["balance"], 1000)
        mock_showinfo.assert_called_once_with("Loan Repayment", "Your loan has been fully repaid!")

    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.simpledialog.askinteger', return_value=1000)
    def test_repay_loan_partial(self, mock_askinteger, mock_showinfo):
        self.user_interface.current_user_data["loan_amount"] = 2000
        self.user_interface.current_user_data["balance"] = 3000
        self.user_interface.repay_loan()
        self.assertEqual(self.user_interface.current_user_data["loan_amount"], 1000)
        self.assertEqual(self.user_interface.current_user_data["balance"], 2000)
        mock_showinfo.assert_called_once_with("Loan Repayment", "Paid 1000 towards loan.")

    def test_update_loan_interest(self):
        self.user_interface.current_user_data["loan_amount"] = 1000
        self.user_interface.current_user_data["loan_start_date"] = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        self.user_interface.current_user_data["interest_rate"] = 1.01
        self.user_interface.update_loan_interest()
        expected_loan_amount = 1000 * (1.01 ** 5)
        self.assertAlmostEqual(self.user_interface.current_user_data["loan_amount"], round(expected_loan_amount, 2))


if __name__ == "__main__":
    unittest.main()
