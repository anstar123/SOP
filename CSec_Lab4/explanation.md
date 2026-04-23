# Decentralized Coupon Sharing Platform - Code Explanation & Viva Guide

## Line-by-Line Code Explanation

### 1. License and Compiler Version
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;
```
- `// SPDX-License-Identifier: MIT`: A machine-readable way to specify the license for the contract. MIT implies open-source.
- `pragma solidity ^0.8.19;`: Specifies the compiler version. The caret (`^`) means it can compile with version 0.8.19 and any newer versions that do not break functionality (up to 0.8.99, but less than 0.9.0).

### 2. Contract Definition
```solidity
// Decentralized Coupon Sharing Platform
contract DecentralizedCouponPlatform {
```
- `contract DecentralizedCouponPlatform {`: Declares a new smart contract named `DecentralizedCouponPlatform`. A contract in Solidity is similar to a class in object-oriented languages.

### 3. Struct Definition for Coupon
```solidity
    // coupon details stored in a struct
    struct Coupon {
        uint256 id;
        string code;           // like "SAVE20" etc.
        string description;
        uint256 discountPercent;
        uint256 expiryTimestamp;
        address owner;         // whoever holds it right now
        address issuedBy;
        bool isRedeemed;
        bool isActive;         // false means revoked
        uint256 issuedAt;
        uint256 redeemedAt;    // 0 if not redeemed yet
    }
```
- `struct Coupon { ... }`: Defines a custom data structure named `Coupon` to group together multiple variables related to a single coupon.
- `uint256 id;`: A unique unsigned integer identifier for the coupon.
- `string code;`: The actual text code for the coupon (e.g., "SAVE20").
- `string description;`: Details about what the coupon does.
- `uint256 discountPercent;`: The discount percentage (1 to 100).
- `uint256 expiryTimestamp;`: The exact UNIX timestamp after which the coupon becomes invalid.
- `address owner;`: The blockchain address of the user who currently holds the coupon.
- `address issuedBy;`: The blockchain address of the platform owner who created the coupon.
- `bool isRedeemed;`: A true/false flag indicating if the coupon has been used.
- `bool isActive;`: A true/false flag indicating if the coupon is still valid (can be manually revoked by setting it to false).
- `uint256 issuedAt;`: The timestamp when the coupon was created.
- `uint256 redeemedAt;`: The timestamp when it was redeemed (starts at 0).

### 4. State Variables
```solidity
    address public owner;
    uint256 private nextCouponId;
```
- `address public owner;`: Stores the address of the platform administrator (who deployed the contract). `public` automatically creates a getter function.
- `uint256 private nextCouponId;`: Keeps track of the ID to assign to the *next* coupon that gets issued. `private` means it cannot be accessed directly from outside the contract.

### 5. Mappings and Arrays
```solidity
    mapping(uint256 => Coupon) public coupons;
    mapping(address => uint256[]) private ownedCoupons;
    mapping(string => bool) private codeExists;   // to avoid duplicate codes
    mapping(address => bool) public authorizedVendors;

    uint256[] private allCouponIds;
```
- `mapping(uint256 => Coupon) public coupons;`: Acts like a dictionary mapping a coupon ID (uint256) to its `Coupon` struct.
- `mapping(address => uint256[]) private ownedCoupons;`: Maps a user's address to a list (array) of coupon IDs they currently own.
- `mapping(string => bool) private codeExists;`: Maps a coupon code string to a boolean. Used to ensure we don't issue duplicate codes (e.g., two "SAVE20" coupons).
- `mapping(address => bool) public authorizedVendors;`: Maps an address to a boolean indicating whether they are allowed to redeem coupons.
- `uint256[] private allCouponIds;`: A list of all coupon IDs ever issued.

### 6. Events
```solidity
    // events for logging everything on chain
    event CouponIssued(uint256 indexed couponId, string code, address indexed issuedTo, uint256 discountPercent, uint256 expiryTimestamp);
    event CouponTransferred(uint256 indexed couponId, address indexed from, address indexed to);
    event CouponRedeemed(uint256 indexed couponId, address indexed redeemedBy, address indexed couponOwner, uint256 timestamp);
    event CouponRevoked(uint256 indexed couponId, address indexed revokedBy);
    event VendorAuthorized(address indexed vendor);
    event VendorRevoked(address indexed vendor);
```
- `event ...`: Events allow smart contracts to log data on the blockchain. External applications (like web interfaces) can listen for these events. The `indexed` keyword allows filtering logs by that specific argument.

### 7. Modifiers
```solidity
    // modifiers for access control

    modifier onlyOwner() {
        require(msg.sender == owner, "Access denied: caller is not the platform owner");
        _;
    }
```
- `modifier onlyOwner() { ... }`: A reusable block of code that runs *before* the function it modifies. It checks if the person calling the function (`msg.sender`) is the `owner`. `_;` tells the execution to return to the original function.

```solidity
    // vendors + owner can redeem
    modifier onlyVendor() {
        require(
            authorizedVendors[msg.sender] || msg.sender == owner,
            "Access denied: caller is not an authorized vendor"
        );
        _;
    }
```
- Ensures the caller is either an authorized vendor or the platform owner.

```solidity
    modifier couponExists(uint256 _id) {
        require(_id < nextCouponId, "Coupon does not exist");
        _;
    }
```
- Ensures the provided `_id` corresponds to a coupon that has been issued (since `nextCouponId` strictly increases).

```solidity
    modifier couponNotRedeemed(uint256 _id) {
        require(!coupons[_id].isRedeemed, "Coupon has already been redeemed");
        _;
    }
```
- Ensures the `isRedeemed` flag of the coupon is `false`.

```solidity
    modifier couponIsActive(uint256 _id) {
        require(coupons[_id].isActive, "Coupon has been revoked by issuer");
        _;
    }
```
- Ensures the coupon has not been manually revoked (`isActive` is true).

```solidity
    modifier couponNotExpired(uint256 _id) {
        require(block.timestamp <= coupons[_id].expiryTimestamp, "Coupon has expired");
        _;
    }
```
- Ensures the current block's timestamp is less than or equal to the coupon's expiration time.

### 8. Constructor
```solidity
    constructor() {
        owner = msg.sender;
        nextCouponId = 0;
        authorizedVendors[msg.sender] = true; // owner is vendor by default
    }
```
- `constructor() { ... }`: A special function that runs only once when the contract is deployed.
- Sets the `owner` to whoever deployed the contract (`msg.sender`).
- Initializes `nextCouponId` to 0.
- Adds the owner to the list of `authorizedVendors`.

### 9. Vendor Management Functions
```solidity
    // ---- Vendor Management (owner only) ----

    function authorizeVendor(address _vendor) external onlyOwner {
        require(_vendor != address(0), "Invalid vendor address");
        require(!authorizedVendors[_vendor], "Vendor already authorized");
        authorizedVendors[_vendor] = true;
        emit VendorAuthorized(_vendor);
    }
```
- Allows the owner to authorize a new vendor.
- Checks against zero address (a burn/unusable address) and ensures the vendor isn't already authorized.
- Emits the `VendorAuthorized` event.

```solidity
    function revokeVendorAuth(address _vendor) external onlyOwner {
        require(authorizedVendors[_vendor], "Address is not a vendor");
        authorizedVendors[_vendor] = false;
        emit VendorRevoked(_vendor);
    }
```
- Allows the owner to remove vendor privileges from an address. Emits `VendorRevoked`.

### 10. Issuing Coupons
```solidity
    // ---- Issuing Coupons (owner only) ----

    function issueCoupon(
        string memory _code,
        string memory _description,
        uint256 _discountPct,
        uint256 _validDays,
        address _recipient
    ) external onlyOwner returns (uint256 couponId) {
```
- `external`: means this function can only be called from outside the contract.
- `onlyOwner`: restricts caller to the contract owner.
- Returns the newly created `couponId`.

```solidity
        require(bytes(_code).length > 0, "Coupon code cannot be empty");
        require(bytes(_description).length > 0, "Description cannot be empty");
        require(_discountPct > 0 && _discountPct <= 100, "Discount must be 1-100");
        require(_validDays > 0, "Validity must be > 0 days");
        require(_recipient != address(0), "Invalid recipient address");
        require(!codeExists[_code], "Coupon code already exists");
```
- A series of input validations. Note that strings must be converted to bytes (`bytes(_code)`) to check their length in Solidity.

```solidity
        couponId = nextCouponId;
        nextCouponId++;

        uint256 expiry = block.timestamp + (_validDays * 1 days);
```
- Grabs the current ID, increments the counter for the next time, and calculates the expiry timestamp.

```solidity
        coupons[couponId] = Coupon({
            id: couponId,
            code: _code,
            description: _description,
            discountPercent: _discountPct,
            expiryTimestamp: expiry,
            owner: _recipient,
            issuedBy: msg.sender,
            isRedeemed: false,
            isActive: true,
            issuedAt: block.timestamp,
            redeemedAt: 0
        });

        codeExists[_code] = true;
        ownedCoupons[_recipient].push(couponId);
        allCouponIds.push(couponId);

        emit CouponIssued(couponId, _code, _recipient, _discountPct, expiry);
    }
```
- Creates the `Coupon` struct and saves it in the `coupons` mapping.
- Marks the code as existing.
- Adds the `couponId` to the recipient's owned list and the global list.
- Emits the `CouponIssued` event.

### 11. Transferring Coupons
```solidity
    // ---- Transfer Coupon (holder only) ----

    function transferCoupon(uint256 _couponId, address _to)
        external
        couponExists(_couponId)
        couponIsActive(_couponId)
        couponNotRedeemed(_couponId)
        couponNotExpired(_couponId)
    {
```
- Uses multiple modifiers to ensure the coupon is perfectly valid before allowing a transfer.

```solidity
        Coupon storage c = coupons[_couponId];
        require(msg.sender == c.owner, "You do not own this coupon");
        require(_to != address(0), "Invalid recipient address");
        require(_to != msg.sender, "Cannot transfer to yourself");
```
- Loads the coupon from storage (so modifications persist).
- Ensures the person trying to transfer it actually owns it, and validates the recipient address.

```solidity
        address previousOwner = c.owner;
        c.owner = _to;

        _removeFromOwnedCoupons(previousOwner, _couponId);
        ownedCoupons[_to].push(_couponId);

        emit CouponTransferred(_couponId, previousOwner, _to);
    }
```
- Updates the owner, handles the array logic to move the ID from the previous owner's list to the new owner's list, and emits an event.

### 12. Redeeming Coupons
```solidity
    // ---- Redeem Coupon (authorized vendors only) ----

    function redeemCoupon(uint256 _couponId)
        external
        onlyVendor
        couponExists(_couponId)
        couponIsActive(_couponId)
        couponNotRedeemed(_couponId)
        couponNotExpired(_couponId)
    {
        Coupon storage c = coupons[_couponId];
        c.isRedeemed = true;
        c.redeemedAt = block.timestamp;

        emit CouponRedeemed(_couponId, msg.sender, c.owner, block.timestamp);
    }
```
- Allows an authorized vendor to mark a valid coupon as redeemed.
- It records the time of redemption and fires an event.

### 13. Revoking Coupons
```solidity
    // ---- Revoke Coupon (owner only) ----

    function revokeCoupon(uint256 _couponId)
        external
        onlyOwner
        couponExists(_couponId)
        couponNotRedeemed(_couponId)
    {
        coupons[_couponId].isActive = false;
        emit CouponRevoked(_couponId, msg.sender);
    }
```
- Allows the owner to manually invalidate a coupon (e.g., if issued by mistake), but only if it hasn't been redeemed yet.

### 14. View Functions (Getters)
```solidity
    // ---- View Functions ----

    function getCoupon(uint256 _couponId) external view couponExists(_couponId) returns (Coupon memory) {
        return coupons[_couponId];
    }
```
- Returns the complete `Coupon` struct for a given ID. `view` means it doesn't modify the blockchain state (costs zero gas when called externally).

```solidity
    function getCouponsOf(address _holder) external view returns (uint256[] memory) {
        return ownedCoupons[_holder];
    }

    function getAllCouponIds() external view returns (uint256[] memory) {
        return allCouponIds;
    }

    function totalCouponsIssued() external view returns (uint256) {
        return nextCouponId;
    }
```
- Simple getter functions to retrieve arrays or counters from the contract state.

```solidity
    // check if coupon is usable right now
    function isCouponValid(uint256 _couponId) external view couponExists(_couponId) returns (bool valid, string memory reason) {
        Coupon storage c = coupons[_couponId];
        if (c.isRedeemed) return (false, "Already redeemed");
        if (!c.isActive)  return (false, "Revoked by issuer");
        if (block.timestamp > c.expiryTimestamp) return (false, "Expired");
        return (true, "Valid");
    }
```
- A convenient helper function for a frontend interface to check why a coupon might not be usable.

### 15. Internal Helper Array Function
```solidity
    // internal helper - removes coupon id from an address's list
    function _removeFromOwnedCoupons(address _holder, uint256 _couponId) internal {
        uint256[] storage arr = ownedCoupons[_holder];
        for (uint256 i = 0; i < arr.length; i++) {
            if (arr[i] == _couponId) {
                arr[i] = arr[arr.length - 1]; // swap with last element and pop
                arr.pop();
                break;
            }
        }
    }
}
```
- `internal`: means it can only be called from within the contract itself (or derived contracts).
- Since removing an element from the middle of an array leaves a gap in Solidity, this function replaces the element-to-delete with the last element in the array, and then `pop()`s the last element off. This is a common pattern for array deletion in Solidity to save gas and avoid empty spaces.

---

## Possible Viva Questions & Answers (QnA)

**Q1: What is the purpose of `pragma solidity ^0.8.19;`?**
**A:** It tells the compiler to use version 0.8.19 or a newer, non-breaking version (up to 0.8.99). This prevents the contract from being compiled with an older compiler that might have unfixed bugs, or a newer major version (like 0.9.0) that might change the syntax and break the code.

**Q2: What is a `struct` in Solidity? Why is it used here?**
**A:** A `struct` is a custom data type that allows grouping multiple variables together. Here, `Coupon` groups the ID, code, description, timestamps, and state flags into one neat unit so that an entire coupon can be passed around and stored easily in a mapping.

**Q3: What is the difference between `memory` and `storage` keywords? (Hint: look at `transferCoupon` and `getCoupon`)**
**A:** 
- `storage` is a reference pointer to data that permanently resides on the blockchain. Modifying a `storage` variable (like `Coupon storage c = coupons[_couponId]`) will directly change the data on the blockchain.
- `memory` is a temporary place to store data during the execution of a function. It gets wiped after the function finishes. `view` functions return structs as `memory`.

**Q4: How does the `onlyOwner` modifier work?**
**A:** A modifier is code that can be run before or after a function. `onlyOwner` checks if `msg.sender` (the person calling the contract) is exactly the `owner` address. If not, it reverts the transaction with an error. The `_;` symbol dictates where the actual body of the attached function should be executed.

**Q5: What is `msg.sender`?**
**A:** It is a global variable in Solidity that holds the address of the account (or another smart contract) that is directly calling the current function.

**Q6: Why do we use `block.timestamp`? Can it be manipulated?**
**A:** It retrieves the current timestamp of the block as set by the miner/validator. It is used here to manage coupon expiry and redemption times. While miners can manipulate it slightly (usually within a ~15-second window), for something like days-long expiration times, this small manipulation is not a security risk.

**Q7: Explain the logic inside the `_removeFromOwnedCoupons` function. Why swap with the last element instead of just deleting it?**
**A:** In Solidity arrays, if you just `delete arr[i]`, it leaves an empty, zeroed-out gap at that index. It doesn't shrink the array size. By swapping the target item with the very last item, and then using `.pop()` to remove the end of the array, we remove the item completely and reduce the array length by 1, keeping the array packed.

**Q8: What are `events` and why do we `emit` them?**
**A:** Events are a way for smart contracts to log activity on the blockchain. They are cheaper than storing data in state variables. Frontends (like a React app using ethers.js) can "listen" to these events to update the UI in real-time when a coupon is issued, transferred, or redeemed.

**Q9: Why do you convert strings to bytes to check their length? (`bytes(_code).length > 0`)**
**A:** In Solidity, native `string` types do not have a built-in `.length` property because strings are essentially dynamic arrays of UTF-8 data. Converting it to `bytes` allows us to count the exact number of bytes and ensure the string isn't empty.

**Q10: What happens if I try to transfer a coupon that has expired?**
**A:** The transaction will fail (revert). The `transferCoupon` function uses the `couponNotExpired` modifier, which checks if `block.timestamp <= coupons[_id].expiryTimestamp`. If expired, it throws the error "Coupon has expired".

**Q11: Who pays for the gas when `redeemCoupon` is called?**
**A:** The authorized vendor who calls the `redeemCoupon` function pays the gas fees for that transaction.

**Q12: Can a vendor issue new coupons?**
**A:** No. The `issueCoupon` function has the `onlyOwner` modifier, meaning only the address that deployed the contract can issue new coupons. Vendors can only redeem them.

**Q13: What does the `view` keyword do in the getter functions?**
**A:** It indicates that the function will only read from the blockchain state and not modify it. Calling a `view` function externally from a frontend application costs no gas.
