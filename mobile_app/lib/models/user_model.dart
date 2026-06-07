class User {
  final int id;
  final String fullName;
  final String email;
  final String role;
  final double balance;

  User({
    required this.id,
    required this.fullName,
    required this.email,
    required this.role,
    required this.balance,
  });

  
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      fullName: json['full_name'],
      email: json['email'],
      role: json['role'],
      balance: (json['balance'] as num).toDouble(),
    );
  }

 
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'full_name': fullName,
      'email': email,
      'role': role,
      'balance': balance,
    };
  }
}
