
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta


# ---------------------- DATA STORAGE ----------------------

books = {}
members = {}
transactions = {}

users = {
    "admin": {"password": "admin", "role": "admin"},
    "user": {"password": "user", "role": "user"}
}

book_counter = 1
member_counter = 1


# ---------------------- MAIN APP ----------------------

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("700x550")

        self.current_role = None

        self.frames = {}

        pages = (
            LoginPage, AdminHome, UserHome,
            AddBookPage, UpdateBookPage, DeleteBookPage,
            AddMemberPage, UpdateMemberPage, DeleteMemberPage,
            SearchBookPage, IssueBookPage, ReturnBookPage
        )

        for Page in pages:
            frame = Page(self)
            self.frames[Page] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(LoginPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


# ---------------------- LOGIN ----------------------

class LoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Login", font=("Arial", 20)).pack(pady=30)

        tk.Label(self, text="Username").pack()
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Password").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(self, text="Login",
                  command=lambda: self.login(parent)).pack(pady=15)

    def login(self, parent):
        u = self.username.get()
        p = self.password.get()

        if u in users and users[u]["password"] == p:
            parent.current_role = users[u]["role"]
            if users[u]["role"] == "admin":
                parent.show_frame(AdminHome)
            else:
                parent.show_frame(UserHome)
        else:
            messagebox.showerror("Error", "Invalid Credentials")


# ---------------------- HOME PAGES ----------------------

class AdminHome(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Admin Dashboard",
                 font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Add Book",
                  command=lambda: parent.show_frame(AddBookPage)).pack(pady=5)

        tk.Button(self, text="Update Book",
                  command=lambda: parent.show_frame(UpdateBookPage)).pack(pady=5)

        tk.Button(self, text="Delete Book",
                  command=lambda: parent.show_frame(DeleteBookPage)).pack(pady=5)

        tk.Button(self, text="Add Member",
                  command=lambda: parent.show_frame(AddMemberPage)).pack(pady=5)

        tk.Button(self, text="Update Member",
                  command=lambda: parent.show_frame(UpdateMemberPage)).pack(pady=5)

        tk.Button(self, text="Delete Member",
                  command=lambda: parent.show_frame(DeleteMemberPage)).pack(pady=5)

        tk.Button(self, text="Search Book",
                  command=lambda: parent.show_frame(SearchBookPage)).pack(pady=5)

        tk.Button(self, text="Issue Book",
                  command=lambda: parent.show_frame(IssueBookPage)).pack(pady=5)

        tk.Button(self, text="Return Book",
                  command=lambda: parent.show_frame(ReturnBookPage)).pack(pady=5)

        tk.Button(self, text="Logout",
                  command=lambda: parent.show_frame(LoginPage)).pack(pady=20)


class UserHome(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="User Dashboard",
                 font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Search Book",
                  command=lambda: parent.show_frame(SearchBookPage)).pack(pady=5)

        tk.Button(self, text="Issue Book",
                  command=lambda: parent.show_frame(IssueBookPage)).pack(pady=5)

        tk.Button(self, text="Return Book",
                  command=lambda: parent.show_frame(ReturnBookPage)).pack(pady=5)

        tk.Button(self, text="Logout",
                  command=lambda: parent.show_frame(LoginPage)).pack(pady=20)


# ---------------------- BOOK CRUD ----------------------

class AddBookPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Add Book", font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Book Name").pack()
        self.name = tk.Entry(self)
        self.name.pack()

        tk.Label(self, text="Author").pack()
        self.author = tk.Entry(self)
        self.author.pack()

        tk.Button(self, text="Add Book",
                  command=self.add_book).pack(pady=10)

        tk.Button(self, text="Back",
                  command=lambda: parent.show_frame(AdminHome)).pack()

    def add_book(self):
        global book_counter

        name = self.name.get()
        author = self.author.get()

        if not name or not author:
            messagebox.showerror("Error", "All fields are required")
            return

        book_id = f"B{book_counter}"
        books[book_id] = {
            "name": name,
            "author": author,
            "available": True
        }
        book_counter += 1

        messagebox.showinfo("Success", f"Book added with ID {book_id}")

        self.name.delete(0, tk.END)
        self.author.delete(0, tk.END)


class UpdateBookPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Update Book",
                 font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Book ID").pack()
        self.book_id = tk.Entry(self)
        self.book_id.pack()

        tk.Button(self, text="Load",
                  command=self.load_book).pack(pady=5)

        tk.Label(self, text="New Name").pack()
        self.name = tk.Entry(self)
        self.name.pack()

        tk.Label(self, text="New Author").pack()
        self.author = tk.Entry(self)
        self.author.pack()

        tk.Button(self, text="Update",
                  command=self.update_book).pack(pady=10)

        tk.Button(self, text="Back",
                  command=lambda: parent.show_frame(AdminHome)).pack()

    def load_book(self):
        bid = self.book_id.get()
        if bid in books:
            self.name.delete(0, tk.END)
            self.author.delete(0, tk.END)
            self.name.insert(0, books[bid]["name"])
            self.author.insert(0, books[bid]["author"])
        else:
            messagebox.showerror("Error", "Book not found")

    def update_book(self):
        bid = self.book_id.get()

        if bid not in books:
            messagebox.showerror("Error", "Invalid Book ID")
            return

        name = self.name.get()
        author = self.author.get()

        if not name or not author:
            messagebox.showerror("Error", "All fields required")
            return

        books[bid]["name"] = name
        books[bid]["author"] = author

        messagebox.showinfo("Success", "Book updated successfully")


class DeleteBookPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Delete Book",
                 font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Book ID").pack()
        self.book_id = tk.Entry(self)
        self.book_id.pack()

        tk.Button(self, text="Delete",
                  command=self.delete_book).pack(pady=10)

        tk.Button(self, text="Back",
                  command=lambda: parent.show_frame(AdminHome)).pack()

    def delete_book(self):
        bid = self.book_id.get()

        if bid not in books:
            messagebox.showerror("Error", "Book not found")
            return

        if not books[bid]["available"]:
            messagebox.showerror("Error", "Cannot delete issued book")
            return

        del books[bid]
        messagebox.showinfo("Success", "Book deleted successfully")


# ---------------------- MEMBER CRUD ----------------------

class AddMemberPage(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Add Member",
                 font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Name").pack()
        self.name = tk.Entry(self)
        self.name.pack()

        self.duration = tk.StringVar(value="6 months")

        tk.Radiobutton(self, text="6 months",
                       variable=self.duration,
                       value="6 months").pack()
        tk.Radiobutton(self, text="1 year",
                       variable=self.duration,
                       value="1 year").pack()
        tk.Radiobutton(self, text="2 years",
                       variable=self.duration,
                       value="2 years").pack()

        tk.Button(self, text="Add Member",
                  command=self.add_member).pack(pady=10)

        tk.Button(self, text="Back",
                  command=lambda: parent.show_frame(AdminHome)).pack()

    def add_member(self):
        global member_counter

        name = self.name.get()

        if not name:
            messagebox.showerror("Error", "Name is required")
            return

        member_id = f"M{member_counter}"
        members[member_id] = {
            "name": name,
            "duration": self.duration.get()
        }
        member_counter += 1

        messagebox.showinfo("Success", f"Member added with ID {member_id}")
        self.name.delete(0, tk.END)

class UpdateMemberPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Update Membership",
                 font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Membership ID").pack()
        self.member_id = tk.Entry(self)
        self.member_id.pack()

        self.option = tk.StringVar(value="extend")

        tk.Radiobutton(self, text="Extend (6 months)",
                       variable=self.option,
                       value="extend").pack()

        tk.Radiobutton(self, text="Cancel Membership",
                       variable=self.option,
                       value="cancel").pack()

        tk.Button(self, text="Update",
                  command=self.update_member).pack(pady=10)

        tk.Button(self, text="Back",
                  command=lambda: parent.show_frame(AdminHome)).pack()

    def update_member(self):
        member_id = self.member_id.get()

        if not member_id:
            messagebox.showerror("Error", "Membership ID is required")
            return

        if member_id not in members:
            messagebox.showerror("Error", "Member not found")
            return

        if self.option.get() == "extend":
            members[member_id]["duration"] = "6 months"
            messagebox.showinfo("Success", "Membership extended by 6 months")

        else:
            del members[member_id]
            messagebox.showinfo("Success", "Membership cancelled")

        self.member_id.delete(0, tk.END)

class DeleteMemberPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Delete Member",
                 font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Membership ID").pack()
        self.member_id = tk.Entry(self)
        self.member_id.pack()

        tk.Button(self, text="Delete",
                  command=self.delete_member).pack(pady=10)

        tk.Button(self, text="Back",
                  command=lambda: parent.show_frame(AdminHome)).pack()

    def delete_member(self):
        member_id = self.member_id.get()

        if not member_id:
            messagebox.showerror("Error", "Membership ID is required")
            return

        if member_id not in members:
            messagebox.showerror("Error", "Member not found")
            return

        del members[member_id]

        messagebox.showinfo("Success", "Member deleted successfully")
        self.member_id.delete(0, tk.END)


# ---------------------- SEARCH / ISSUE / RETURN ----------------------

class SearchBookPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Search Book",
                 font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Enter Book Name").pack()
        self.search = tk.Entry(self)
        self.search.pack()

        tk.Button(self, text="Search",
                  command=self.search_book).pack(pady=10)

        self.result = tk.Label(self, text="")
        self.result.pack()

        tk.Button(self, text="Back",
                  command=lambda: parent.show_frame(
                      AdminHome if parent.current_role == "admin" else UserHome
                  )).pack()

    def search_book(self):
        name = self.search.get()

        if not name:
            messagebox.showerror("Error", "Enter book name")
            return

        for bid, book in books.items():
            if name.lower() in book["name"].lower():
                self.result.config(
                    text=f"{bid} | {book['name']} by {book['author']} | Available: {book['available']}")
                return

        self.result.config(text="Book not found")


class IssueBookPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Issue Book",
                 font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Book ID").pack()
        self.book_id = tk.Entry(self)
        self.book_id.pack()

        tk.Label(self, text="Member ID").pack()
        self.member_id = tk.Entry(self)
        self.member_id.pack()

        tk.Button(self, text="Issue",
                  command=self.issue_book).pack(pady=10)

        tk.Button(self, text="Back",
                  command=lambda: parent.show_frame(
                      AdminHome if parent.current_role == "admin" else UserHome
                  )).pack()

    def issue_book(self):
        bid = self.book_id.get()
        mid = self.member_id.get()

        if bid not in books:
            messagebox.showerror("Error", "Invalid Book ID")
            return

        if mid not in members:
            messagebox.showerror("Error", "Invalid Member ID")
            return

        if not books[bid]["available"]:
            messagebox.showerror("Error", "Book already issued")
            return

        issue_date = datetime.now()
        return_date = issue_date + timedelta(days=15)

        transactions[bid] = {
            "member_id": mid,
            "issue_date": issue_date,
            "return_date": return_date
        }

        books[bid]["available"] = False
        messagebox.showinfo("Success", "Book issued successfully")


class ReturnBookPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="Return Book",
                 font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text="Book ID").pack()
        self.book_id = tk.Entry(self)
        self.book_id.pack()

        self.fine_paid = tk.IntVar()

        tk.Checkbutton(self, text="Fine Paid",
                       variable=self.fine_paid).pack()

        tk.Button(self, text="Return",
                  command=self.return_book).pack(pady=10)

        tk.Button(self, text="Back",
                  command=lambda: parent.show_frame(
                      AdminHome if parent.current_role == "admin" else UserHome
                  )).pack()

    def return_book(self):
        bid = self.book_id.get()

        if bid not in transactions:
            messagebox.showerror("Error", "Invalid transaction")
            return

        today = datetime.now()
        due_date = transactions[bid]["return_date"]

        delay = (today - due_date).days
        fine = delay * 10 if delay > 0 else 0

        if fine > 0 and self.fine_paid.get() == 0:
            messagebox.showerror("Error",
                                 f"Fine ₹{fine} pending. Please mark as paid.")
            return

        books[bid]["available"] = True
        del transactions[bid]

        messagebox.showinfo("Success", "Book returned successfully")


# ---------------------- RUN PROGRAM ----------------------

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()