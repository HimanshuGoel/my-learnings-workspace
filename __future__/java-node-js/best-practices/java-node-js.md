# Best Practices

- Prioritize Stability: Don't Break Users - Once released, avoid breaking changes. Additive changes are okay.

**Good:** Adding a new optional field `middleName` to a `User` object.

```json
{
  "firstName": "John",
  "lastName": "Doe",
  "middleName": "Patrick"  // new, optional
}
```

**Bad:** Renaming `lastName` to `surname` — existing clients will break.

- Version Only When Necessary - Avoid excessive versioning. Make additive changes first.

**Good:** Add a new optional endpoint `/users/{id}/details` instead of creating `/v2/users/{id}`.

**Bad:** Increment the API version for every minor change.

- Design for Familiarity - Keep endpoints, naming, and behavior intuitive.

**Good:** `/users/{id}/orders` clearly returns a user's orders.

**Bad:** `/getUserOrdersList?id={id}` is verbose and inconsistent.

- Rate Limiting & Safety - Protect API and inform users about limits.

```text
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 750
Retry-After: 60
```

- Paginate Large Data - Use cursor-based pagination for large lists. Returns next page cursor in response for efficient navigation.

```http
GET /users?cursor=eyJpZCI6MTAwfQ
```

- Make Expensive Fields Optional - Avoid sending heavy data unless requested. By default, `profilePicture` and `activityLog` are excluded.

```http
GET /users?include=profilePicture,activityLog
```
