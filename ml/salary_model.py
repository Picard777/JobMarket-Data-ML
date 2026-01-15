import sqlite3 
import pandas as pd 
import torch 
from torch import nn 
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

conn = sqlite3.connect("data/jobs.db")
df = pd.read_sql("SELECT * FROM jobs", conn)
conn.close()

X = df[["year", "experience_level", "company_size"]]
X = pd.get_dummies(X, drop_first=True)
X = X.astype(float)

y = df["salary"]

#Train and test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
#Creating tensors
X_train_t = torch.tensor(X_train.values, dtype=torch.float32)
X_test_t = torch.tensor(X_test.values, dtype=torch.float32)

y_train_t = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
y_test_t = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

#Model
class SalaryRegressor(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, 1)
        
    def forward(self, x):
        return self.linear(x)
model = SalaryRegressor(X_train_t.shape[1])

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

epochs = 300

for epoch in range(epochs):
    model.train()
    
    optimizer.zero_grad()
    outputs = model(X_train_t)
    loss = criterion(outputs, y_train_t)
    
    loss.backward()
    optimizer.step()
    
    if (epoch + 1) % 50 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item(): .2f}")
    
#Evaluation

model.eval()
with torch.no_grad():
    predictions = model(X_test_t).numpy()
    
mae = mean_absolute_error(y_test, predictions)
print(f"Test MAE: {mae: .2f}")
