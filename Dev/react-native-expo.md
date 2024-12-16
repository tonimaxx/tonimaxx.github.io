# 📱 React Native with Expo Cheatsheet

## 🚀 Getting Started

### Installation & Setup
```bash
# Install Expo CLI
npm install -g expo-cli

# Create a new project
npx create-expo-app MyApp
cd MyApp

# Alternative with TypeScript template
npx create-expo-app MyApp --template expo-template-blank-typescript

# Start development server
npx expo start
```

### Project Structure
```plaintext
MyApp/
├── App.js               # Root component
├── app.json            # Expo configuration
├── assets/             # Images, fonts, etc.
├── babel.config.js     # Babel configuration
├── package.json        # Dependencies
└── node_modules/       # Installed packages
```

## 📱 Development Commands

### Basic Commands
```bash
# Start development server
npx expo start

# Start with specific platform
npx expo start --android
npx expo start --ios
npx expo start --web

# Build standalone apps
eas build --platform ios
eas build --platform android

# Eject from Expo managed workflow
npx expo eject

# Install dependencies
npx expo install [package-name]

# Update Expo SDK
npx expo upgrade
```

### Development Tools
```bash
# Start development server with clear cache
npx expo start -c

# Start with tunnel connection
npx expo start --tunnel

# Publishing
npx expo publish

# Generate native code
npx expo prebuild
```

## 📦 Essential Expo Packages

### Navigation
```bash
# Install navigation packages
npx expo install @react-navigation/native
npx expo install @react-navigation/native-stack
npx expo install @react-navigation/bottom-tabs
```

### Common Packages
```bash
# Async storage
npx expo install @react-native-async-storage/async-storage

# Image picker
npx expo install expo-image-picker

# Camera
npx expo install expo-camera

# Location
npx expo install expo-location

# Notifications
npx expo install expo-notifications

# Font loading
npx expo install expo-font

# File system
npx expo install expo-file-system

# SQLite
npx expo install expo-sqlite
```

## 🎨 Core Components

### Basic Components
```jsx
// View - Container component
<View style={styles.container}>
  {/* Child components */}
</View>

// Text - Text display
<Text style={styles.text}>Hello World</Text>

// Image - Image display
<Image 
  source={require('./assets/image.png')}
  style={styles.image}
/>

// TouchableOpacity - Touchable component
<TouchableOpacity onPress={() => console.log('Pressed')}>
  <Text>Press Me</Text>
</TouchableOpacity>

// TextInput - User input
<TextInput
  value={text}
  onChangeText={setText}
  placeholder="Enter text"
  style={styles.input}
/>

// ScrollView - Scrollable container
<ScrollView style={styles.scrollView}>
  {/* Scrollable content */}
</ScrollView>

// FlatList - Efficient list rendering
<FlatList
  data={items}
  renderItem={({ item }) => <Item item={item} />}
  keyExtractor={item => item.id}
/>
```

### Styling
```jsx
// StyleSheet creation
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontSize: 16,
    color: '#000',
  },
});

// Inline styles
<View style={{ flex: 1, padding: 20 }}>
  {/* Content */}
</View>

// Multiple styles
<View style={[styles.container, styles.padding]}>
  {/* Content */}
</View>
```

## 🧭 Navigation Examples

### Stack Navigation
```jsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{ title: 'Welcome' }}
        />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Navigation in screens
function HomeScreen({ navigation }) {
  return (
    <Button
      title="Go to Details"
      onPress={() => navigation.navigate('Details', { id: 123 })}
    />
  );
}
```

### Tab Navigation
```jsx
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Tab = createBottomTabNavigator();

function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Home" component={HomeScreen} />
        <Tab.Screen name="Settings" component={SettingsScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

## 📱 Common Hooks

### State Management
```jsx
// useState
const [count, setCount] = useState(0);

// useEffect
useEffect(() => {
  // Component did mount
  return () => {
    // Component will unmount
  };
}, []);

// useContext
const value = useContext(MyContext);

// Custom hook example
function useAPI() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  return { data, loading };
}
```

## 📱 Platform Specific Code

### Platform Detection
```jsx
import { Platform } from 'react-native';

// Platform-specific code
const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === 'ios' ? 20 : 0,
  },
});

// Platform-specific component
const Component = Platform.select({
  ios: () => require('./Component.ios'),
  android: () => require('./Component.android'),
})();

// Platform-specific file extensions
// Component.ios.js
// Component.android.js
```

## 🔧 Debugging

### Development Tools
```bash
# Enable remote debugging
// Shake device or press ⌘D in iOS simulator
// Press ⌘M in Android simulator

# View logs
console.log('Debug message');
console.warn('Warning message');
console.error('Error message');

# Performance monitoring
console.time('operationName');
// ... code to measure
console.timeEnd('operationName');
```

## 📦 Publishing

### EAS Build
```bash
# Configure EAS
eas build:configure

# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# Submit to stores
eas submit -p ios
eas submit -p android
```

## 🏗️ Best Practices

### Performance Optimization
```jsx
// Use memo for expensive computations
const memoizedValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);

// Use callback for function props
const memoizedCallback = useCallback(
  () => {
    doSomething(a, b);
  },
  [a, b],
);

// Use FlatList instead of ScrollView for long lists
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={item => item.id}
  initialNumToRender={10}
  maxToRenderPerBatch={10}
  windowSize={5}
/>
```

### Error Handling
```jsx
// Error Boundary
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <Text>Something went wrong</Text>;
    }
    return this.props.children;
  }
}

// Try-Catch in async functions
async function fetchData() {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}
```

Remember to:
1. Always test on both iOS and Android
2. Handle different screen sizes and orientations
3. Implement proper error handling
4. Follow platform-specific design guidelines
5. Optimize performance for production builds
6. Keep Expo SDK and dependencies updated
7. Use TypeScript for better type safety
8. Implement proper security measures